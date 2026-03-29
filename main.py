import threading
import json
import time

from config import DEVICES, API_HOST, API_PORT, INTERVAL_SECONDS
from collector.ssh import collect_raw
from collector.parser import build_result
from api.app import app, set_metrics


def collect_host(device: dict):
    host = device['host']
    try:
        print(f'[collector] Zbieram dane z {host}...')
        raw    = collect_raw(device)
        result = build_result(host, raw)

        set_metrics(host, result)

        with open(f'metrics_{host}.json', 'w') as f:
            json.dump(result, f, indent=4)
        
        print(f'[collector] Dane zebrane: {json.dumps(result, indent=4)}')

    except Exception as e:
        print(f'[collector] Błąd podczas zbierania danych: {e}')
        
def collection_loop():
    while True:
        threads = []
        for device in DEVICES:
            t = threading.Thread(target=collect_host, args=(device,), daemon=True)
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()

        time.sleep(INTERVAL_SECONDS)


def main():
    print(f"Monitor startuje — interwał: {INTERVAL_SECONDS}s")
    print(f"API: http://localhost:{API_PORT}/metrics\n")

    #collector in background thread to not block Flask
    threading.Thread(target=collection_loop, daemon=True).start()

    #flask app in main thread
    app.run(host=API_HOST, port=API_PORT)

if __name__ == '__main__':
    main()