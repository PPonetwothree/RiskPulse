import sqlite3
import json
import time
import threading
from datetime import datetime, timedelta
import random


class DatabaseManager:
    """SQLite-based database manager. Thread-safe via connection-per-thread."""

    def __init__(self, config):
        self.db_path = config.get('path', 'riskpulse.db')
        self._local = threading.local()
        self._init_db()

    def _get_conn(self):
        if not hasattr(self._local, 'conn') or self._local.conn is None:
            self._local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._local.conn.row_factory = sqlite3.Row
        return self._local.conn

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                event_type TEXT,
                country TEXT,
                location TEXT,
                summary TEXT,
                severity TEXT,
                fatalities INTEGER DEFAULT 0,
                sentiment_score REAL,
                collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS sentiment_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                country TEXT NOT NULL,
                current_score REAL,
                baseline_score REAL,
                shift REAL,
                events_analyzed INTEGER,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS forecasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                country TEXT NOT NULL,
                forecast_values TEXT,
                risk_score REAL,
                baseline REAL,
                arima_values TEXT,
                prophet_values TEXT,
                lstm_values TEXT,
                horizon_days INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_type TEXT,
                country TEXT,
                severity TEXT,
                message TEXT,
                value REAL,
                suppressed INTEGER DEFAULT 0,
                triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        conn.close()

    def insert_events(self, events):
        conn = self._get_conn()
        conn.executemany("""
            INSERT INTO events (source, event_type, country, location, summary, severity, fatalities, sentiment_score)
            VALUES (:source, :event_type, :country, :location, :summary, :severity, :fatalities, :sentiment_score)
        """, events)
        conn.commit()

    def insert_social_posts(self, posts):
        conn = self._get_conn()
        conn.executemany("""
            INSERT INTO events (source, event_type, country, location, summary, severity, fatalities, sentiment_score)
            VALUES (:source, :event_type, :country, :location, :summary, :severity, 0, :sentiment_score)
        """, posts)
        conn.commit()

    def get_unprocessed_events(self, limit=100):
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT * FROM events WHERE processed=0 ORDER BY collected_at DESC LIMIT ?",
            (limit,)
        ).fetchall()
        return [dict(r) for r in rows]

    def mark_events_processed(self, ids):
        if not ids:
            return
        conn = self._get_conn()
        placeholders = ','.join('?' * len(ids))
        conn.execute(f"UPDATE events SET processed=1 WHERE id IN ({placeholders})", ids)
        conn.commit()

    def get_recent_events(self, limit=50):
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT * FROM events ORDER BY collected_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]

    def get_event_counts_by_country(self, days=90):
        conn = self._get_conn()
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()
        rows = conn.execute("""
            SELECT country, DATE(collected_at) as day, COUNT(*) as count
            FROM events
            WHERE collected_at >= ?
            GROUP BY country, day
            ORDER BY country, day
        """, (since,)).fetchall()
        return [dict(r) for r in rows]

    def insert_sentiment(self, country, current, baseline, shift, count):
        conn = self._get_conn()
        conn.execute("""
            INSERT INTO sentiment_analysis (country, current_score, baseline_score, shift, events_analyzed)
            VALUES (?, ?, ?, ?, ?)
        """, (country, current, baseline, shift, count))
        conn.commit()

    def get_latest_sentiment_analysis(self):
        conn = self._get_conn()
        rows = conn.execute("""
            SELECT s1.* FROM sentiment_analysis s1
            INNER JOIN (
                SELECT country, MAX(analyzed_at) as max_at
                FROM sentiment_analysis GROUP BY country
            ) s2 ON s1.country = s2.country AND s1.analyzed_at = s2.max_at
            ORDER BY ABS(s1.shift) DESC
        """).fetchall()
        countries = [dict(r) for r in rows]
        return {'countries': countries}

    def insert_forecast(self, country, forecast_values, risk_score, baseline,
                        arima, prophet, lstm, horizon_days):
        conn = self._get_conn()
        conn.execute("""
            INSERT INTO forecasts (country, forecast_values, risk_score, baseline,
                arima_values, prophet_values, lstm_values, horizon_days)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            country,
            json.dumps(forecast_values),
            risk_score,
            baseline,
            json.dumps(arima),
            json.dumps(prophet),
            json.dumps(lstm),
            horizon_days
        ))
        conn.commit()

    def get_latest_forecast(self, country=None):
        conn = self._get_conn()
        if country:
            row = conn.execute(
                "SELECT * FROM forecasts WHERE country=? ORDER BY created_at DESC LIMIT 1",
                (country,)
            ).fetchone()
            if row:
                r = dict(row)
                r['forecast_values'] = json.loads(r['forecast_values'])
                return r
            return None
        else:
            rows = conn.execute("""
                SELECT f1.* FROM forecasts f1
                INNER JOIN (
                    SELECT country, MAX(created_at) as max_at
                    FROM forecasts GROUP BY country
                ) f2 ON f1.country = f2.country AND f1.created_at = f2.max_at
                ORDER BY f1.risk_score DESC
            """).fetchall()
            result = []
            for row in rows:
                r = dict(row)
                r['forecast_values'] = json.loads(r['forecast_values'])
                result.append(r)
            return result

    def insert_alert(self, alert_type, country, severity, message, value=0, suppressed=False):
        conn = self._get_conn()
        conn.execute("""
            INSERT INTO alerts (alert_type, country, severity, message, value, suppressed)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (alert_type, country, severity, message, value, int(suppressed)))
        conn.commit()

    def get_last_alert_time(self, country, alert_type):
        conn = self._get_conn()
        row = conn.execute("""
            SELECT triggered_at FROM alerts
            WHERE country=? AND alert_type=? AND suppressed=0
            ORDER BY triggered_at DESC LIMIT 1
        """, (country, alert_type)).fetchone()
        if row:
            return datetime.fromisoformat(row['triggered_at'])
        return None

    def get_recent_alerts(self, limit=20):
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT * FROM alerts WHERE suppressed=0 ORDER BY triggered_at DESC LIMIT ?",
            (limit,)
        ).fetchall()
        return [dict(r) for r in rows]

    def get_event_count_by_country(self, country, hours=24):
        conn = self._get_conn()
        since = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
        row = conn.execute(
            "SELECT COUNT(*) as cnt FROM events WHERE country=? AND collected_at >= ?",
            (country, since)
        ).fetchone()
        return row['cnt'] if row else 0
