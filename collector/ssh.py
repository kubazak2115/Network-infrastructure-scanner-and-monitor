from netmiko import ConnectHandler
import subprocess
import json
import os
import platform

def collect_raw(device: dict) -> dict:
    connection = ConnectHandler(**device)

    raw = {
        'ifconfig':  connection.send_command('ifconfig'),
        'cpu':       connection.send_command('cat /proc/stat | head -1'),
        'ram':       connection.send_command('free -m'),
        'hostname':  connection.send_command('hostname'),
    }

    connection.disconnect()

    return raw

def run_scanner(subnet: str, start: int, end: int) -> list:
    try:
        binary = './scanner/scanner.exe' if platform.system() == 'Windows' else './scanner/scanner'
        result = subprocess.run(
            [binary, subnet, str(start), str(end)],
            capture_output=True, text=True, timeout=30
        )

        json_line = result.stdout.strip().split('\n')[-1]

        all_hosts = json.loads(json_line)
        
        return [h for h in all_hosts if h.get('alive')]

    except Exception as e:
        print(f'[scanner] Błąd podczas skanowania: {e}')
        return []