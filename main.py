import threading
import json

from config import DEVICE, API_HOST, API_PORT
from collector.ssh import collect_raw
from collector.parser import build_result
from api.app import app, set_metrics

def main():
    print(f"Łączę z {DEVICE['host']}...")
    raw    = collect_raw(DEVICE)
    result = build_result(DEVICE['host'], raw)

    set_metrics(result)

    with open('metrics.json', 'w') as f:
        json.dump(result, f, indent=4)

    print(json.dumps(result, indent=4))
    print(f"\nAPI działa na http://localhost:{API_PORT}/metrics")

    threading.Thread(
        target=lambda: app.run(host=API_HOST, port=API_PORT),
        daemon=True
    ).start()

    input("Wciśnij Enter żeby zatrzymać...\n")

if __name__ == '__main__':
    main()