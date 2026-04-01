import json
import time
import queue
import logging
from datetime import datetime

import yaml
from flask import Flask, render_template, Response, jsonify, request

from agents.message_bus import MessageBus
from agents.collector_agent import CollectorAgent
from agents.analyzer_agent import AnalyzerAgent
from agents.forecaster_agent import ForecastAgent
from agents.alert_manager_agent import AlertManagerAgent
from utils.database import DatabaseManager
from utils.logger import setup_logger

# ─── Setup ───────────────────────────────────────────────────────────
setup_logger()
logger = logging.getLogger('riskpulse.app')

with open('config.yaml') as f:
    config = yaml.safe_load(f)

app = Flask(__name__)

db = DatabaseManager(config['database'])
message_bus = MessageBus()

agents = {
    'collector': CollectorAgent(message_bus, db, config),
    'analyzer': AnalyzerAgent(message_bus, db, config),
    'forecaster': ForecastAgent(message_bus, db, config),
    'alerts': AlertManagerAgent(message_bus, db, config),
}

message_bus.start_listening()
for agent in agents.values():
    agent.start()

logger.info('All agents started — dashboard ready')


# ─── SSE Event mapping ──────────────────────────────────────────────

def _topic_to_sse_event(topic):
    if 'agent.' in topic and '.status' in topic:
        return 'agent_status'
    if 'collector.' in topic and '.complete' in topic:
        return 'events_collected'
    if 'analyzer.sentiment.complete' in topic:
        return 'sentiment_analyzed'
    if 'analyzer.alert.shift' in topic:
        return 'sentiment_alert'
    if 'forecaster.complete' in topic:
        return 'forecast_updated'
    if 'forecaster.alert.high_risk' in topic:
        return 'forecast_alert'
    if 'alert.triggered' in topic:
        return 'alert_triggered'
    if 'alertmgr.heartbeat' in topic:
        return 'alert_heartbeat'
    return 'system'


# ─── Routes ─────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/stream')
def stream():
    """Server-Sent Events endpoint — streams real-time updates to the dashboard."""
    def event_generator():
        # Send a connected ping
        yield 'event: connected\ndata: {"status": "connected"}\n\n'

        client_queue = queue.Queue(maxsize=200)

        def on_message(topic, data):
            try:
                client_queue.put_nowait({'topic': topic, 'data': data})
            except queue.Full:
                pass

        # Subscribe to all interesting topics
        for pattern in ['agent.*.status', 'collector.*.complete', 'collector.error',
                        'analyzer.*', 'forecaster.*', 'alert.*', 'alertmgr.*']:
            message_bus.subscribe(pattern, on_message)

        try:
            while True:
                try:
                    msg = client_queue.get(timeout=15)
                    event_type = _topic_to_sse_event(msg['topic'])
                    payload = json.dumps(msg['data'])
                    yield f'event: {event_type}\ndata: {payload}\n\n'
                except queue.Empty:
                    # Keep-alive comment
                    yield ': keepalive\n\n'
        except GeneratorExit:
            pass

    return Response(
        event_generator(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
        }
    )


@app.route('/api/state')
def api_state():
    """Full initial dashboard state."""
    sentiment = db.get_latest_sentiment_analysis()
    forecasts = db.get_latest_forecast()
    recent_events = db.get_recent_events(limit=30)
    recent_alerts = db.get_recent_alerts(limit=15)

    agent_info = {name: agent.get_info() for name, agent in agents.items()}

    return jsonify({
        'sentiment': sentiment,
        'forecasts': forecasts,
        'recent_events': recent_events,
        'alerts': recent_alerts,
        'agents': agent_info,
        'server_time': datetime.utcnow().isoformat()
    })


@app.route('/api/agents')
def api_agents():
    return jsonify({name: agent.get_info() for name, agent in agents.items()})


@app.route('/api/agents/<agent_name>/<action>', methods=['POST'])
def control_agent(agent_name, action):
    if agent_name not in agents:
        return jsonify({'error': 'Agent not found'}), 404

    agent = agents[agent_name]

    if action == 'start':
        agent.start()
    elif action == 'stop':
        agent.stop()
    elif action == 'restart':
        agent.stop()
        time.sleep(1)
        agent.start()
    else:
        return jsonify({'error': 'Invalid action'}), 400

    return jsonify({'status': 'ok', 'agent': agent.get_info()})


@app.route('/api/events')
def api_events():
    limit = request.args.get('limit', 50, type=int)
    return jsonify(db.get_recent_events(limit=limit))


@app.route('/api/alerts')
def api_alerts():
    limit = request.args.get('limit', 20, type=int)
    return jsonify(db.get_recent_alerts(limit=limit))


if __name__ == '__main__':
    logger.info('Starting RiskPulse Intelligence Dashboard on http://localhost:8080')
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True, use_reloader=False)
