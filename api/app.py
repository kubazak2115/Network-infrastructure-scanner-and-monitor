from flask import Flask, jsonify

app = Flask(__name__)
_metrics = {}

def set_metrics(host: str, data: dict):
    global _metrics
    _metrics[host] = data

@app.route('/metrics', methods=['GET'])
def get_metrics():
    return jsonify(_metrics)

@app.route('/metrics/<host>', methods=['GET'])
def get_metrics_host(host: str):
    if host not in _metrics:
        return jsonify({'error': 'Host not found'}), 404
    return jsonify(_metrics[host])

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'hosts monitored': list(_metrics.keys())
    })