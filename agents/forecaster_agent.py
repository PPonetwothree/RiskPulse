import random
import math
from agents.base_agent import BaseAgent
from collectors.simulator import generate_historical_series, COUNTRY_BASE_RISK

COUNTRIES = ['SY', 'UA', 'YE', 'SD', 'ET', 'AF', 'IQ', 'ML', 'MM', 'SO']


def _simple_arima(series, steps=7):
    """Simplified ARIMA-like forecast using differencing + AR(1)."""
    if len(series) < 10:
        return [series[-1]] * steps

    # First differences
    diffs = [series[i] - series[i - 1] for i in range(1, len(series))]
    mean_diff = sum(diffs[-14:]) / 14  # trailing 2-week mean

    forecasts = []
    last = series[-1]
    for _ in range(steps):
        noise = random.gauss(0, max(1, last * 0.05))
        last = max(1, last + mean_diff + noise)
        forecasts.append(round(last, 1))
    return forecasts


def _prophet_like(series, steps=7):
    """Prophet-like: trend + weekly seasonality."""
    n = len(series)
    trend_slope = (series[-1] - series[-min(30, n)]) / min(30, n)
    last = series[-1]
    forecasts = []
    for i in range(steps):
        weekly = 2 * math.sin(2 * math.pi * i / 7)
        noise = random.gauss(0, max(1, last * 0.04))
        val = max(1, last + trend_slope * (i + 1) + weekly + noise)
        forecasts.append(round(val, 1))
    return forecasts


def _lstm_like(series, steps=7):
    """LSTM-like: exponential smoothing with momentum."""
    alpha, beta = 0.3, 0.1
    level = series[-1]
    trend = (series[-1] - series[-min(7, len(series))]) / min(7, len(series))

    forecasts = []
    for _ in range(steps):
        noise = random.gauss(0, max(1, level * 0.06))
        level = alpha * (level + trend) + (1 - alpha) * level
        trend = beta * (level - (forecasts[-1] if forecasts else series[-1])) + (1 - beta) * trend
        forecasts.append(round(max(1, level + noise), 1))
    return forecasts


def _ensemble(arima, prophet, lstm, weights=(0.3, 0.3, 0.4)):
    """Weighted ensemble of the three forecasts."""
    result = []
    for a, p, l in zip(arima, prophet, lstm):
        result.append(round(weights[0] * a + weights[1] * p + weights[2] * l, 1))
    return result


class ForecastAgent(BaseAgent):
    """AGENT 3 — FORECASTER-01: Generates 7-day conflict forecasts using ensemble models."""

    def __init__(self, message_bus, db, config):
        super().__init__('FORECASTER-01', message_bus, db)
        self.config = config
        self.threshold = config.get('forecasting', {}).get('high_risk_threshold', 0.65)
        self.interval = config.get('forecasting', {}).get('forecast_interval', 120)
        self.horizon = config.get('forecasting', {}).get('horizon_days', 7)

        # Pre-generate historical series for all countries
        self._history = {c: generate_historical_series(c, days=90) for c in COUNTRIES}

    def get_subscriptions(self):
        return ['analyzer.sentiment.complete']

    def handle_message(self, topic, data):
        pass  # Will naturally run on its schedule

    def get_cycle_interval(self):
        return self.interval

    def execute_cycle(self):
        self.set_status('FORECASTING')
        forecasts = []

        try:
            for country in COUNTRIES:
                series = self._get_series(country)
                if len(series) < 7:
                    continue

                self.set_status(f'MODELING_{country}')

                arima = _simple_arima(series, self.horizon)
                prophet = _prophet_like(series, self.horizon)
                lstm = _lstm_like(series, self.horizon)
                ens = _ensemble(arima, prophet, lstm)

                baseline = sum(series[-30:]) / 30
                risk_score = min(1.0, max(ens) / max(baseline * 1.5, 1))

                self.db.insert_forecast(
                    country=country,
                    forecast_values=ens,
                    risk_score=round(risk_score, 3),
                    baseline=round(baseline, 1),
                    arima=arima,
                    prophet=prophet,
                    lstm=lstm,
                    horizon_days=self.horizon
                )

                forecast_info = {
                    'country': country,
                    'forecast': ens,
                    'arima': arima,
                    'prophet': prophet,
                    'lstm': lstm,
                    'risk_score': round(risk_score, 3),
                    'baseline': round(baseline, 1),
                    'horizon_days': self.horizon
                }
                forecasts.append(forecast_info)

                # Append simulated new day to rolling history
                noise = random.gauss(0, 2)
                self._history[country].append(max(1, int(series[-1] + noise)))
                self._history[country] = self._history[country][-90:]  # keep 90 days

                # High-risk alert
                if risk_score >= self.threshold:
                    self.publish_event('forecaster.alert.high_risk', {
                        'country': country,
                        'risk_score': round(risk_score, 3),
                        'forecast': ens,
                        'baseline': round(baseline, 1)
                    })

            self.publish_event('forecaster.complete', {
                'countries_forecasted': len(forecasts),
                'forecasts': forecasts
            })

        except Exception as e:
            self.logger.error(f'Forecast failed: {e}', exc_info=True)
        finally:
            self.set_status('IDLE')

    def _get_series(self, country):
        """Merge historical simulation with real DB counts if available."""
        db_data = self.db.get_event_counts_by_country(days=30)
        by_country = {}
        for row in db_data:
            if row['country'] == country:
                by_country[row['day']] = row['count']

        if by_country:
            # Blend DB counts into history tail
            recent = list(by_country.values())
            base = self._history[country][:-len(recent)] + recent
            return base
        return self._history[country]
