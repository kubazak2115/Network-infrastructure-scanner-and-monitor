from flask import Flask, jsonify, request, render_template, Blueprint
from collector.ssh import run_scanner
from config import SCAN_SUBNET, SCAN_START, SCAN_END
import threading

app = Flask(__name__, template_folder='../templates', static_folder='../static')

_metrics = {}
_metrics_lock = threading.Lock()

### functions for collector to set metrics

def set_metrics(host: str, data: dict):
    with _metrics_lock:
        _metrics[host] = data

def get_metrics_snapshot() -> dict:
    with _metrics_lock:
        return dict(_metrics)

### frontend route

@app.route('/')
def index():
    return render_template('index.html')

### API endpoints

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/metrics', methods=['GET'])
def get_metrics():
    return jsonify(get_metrics_snapshot())

@api.route('/metrics/<host>', methods=['GET'])
def get_metrics_host(host: str):
    snapshot = get_metrics_snapshot()
    if host not in snapshot:
        return jsonify({'error': 'Host not found'}), 404
    return jsonify(snapshot[host])

@api.route('/health', methods=['GET'])
def health_check():
    snapshot = get_metrics_snapshot()
    return jsonify({
        'status': 'ok',
        'hosts_monitored': list(snapshot.keys())
    })

@api.route('/scan', methods=['GET'])
def scan():
    subnet = request.args.get('subnet', SCAN_SUBNET)
    start  = int(request.args.get('start', SCAN_START))
    end    = int(request.args.get('end', SCAN_END))
    
    results = run_scanner(subnet, start, end)
    return jsonify({
        'subnet': subnet,
        'scanned': f'{subnet}{start}-{subnet}{end}',
        'hosts': results
    })

app.register_blueprint(api)
