from netmiko import ConnectHandler

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