from flask import Flask, jsonify

app = Flask(__name__)
_metrics = {}

def set_metrics(metrics):
    global _metrics
    _metrics = metrics

@app.route('/metrics', methods=['GET'])
def get_metrics():
    return jsonify(_metrics)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})