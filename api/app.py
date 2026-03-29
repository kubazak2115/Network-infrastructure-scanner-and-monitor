from flask import Flask, jsonify, request
from collector.ssh import run_scanner
import platform

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

@app.route('/scan', methods=['GET'])
def scan():
    subnet = request.args.get('subnet', '10.0.1.')
    start = int(request.args.get('start', '90'))
    end   = int(request.args.get('end', '110'))
    
    results = run_scanner(subnet, start, end)
    return jsonify({
        'subnet': subnet,
        'scanned': f'{subnet}{start}-{subnet}{end}',
        'hosts': results
    })
