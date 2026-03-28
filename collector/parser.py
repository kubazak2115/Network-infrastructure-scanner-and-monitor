from datetime import datetime

def parse_interfaces(raw_ifconfig: str) -> dict:
    interfaces = {}
    current_interface = None
    lines = raw_ifconfig.split('\n')

    for line in lines:
        if line and not line.startswith(' '):
            current_interface = line.split()[0]
            interfaces[current_interface] = {}
        elif current_interface:
            if 'inet ' in line:
                interfaces[current_interface]['ip_address'] = line.split()[1]
            elif 'ether ' in line:
                interfaces[current_interface]['mac_address'] = line.split()[1]

    return interfaces

def parse_cpu(raw_cpu: str) -> float:
    cpu_values = raw_cpu.split()
    user   = int(cpu_values[1])
    nice   = int(cpu_values[2])
    system = int(cpu_values[3])
    idle   = int(cpu_values[4])

    total = user + nice + system + idle
    cpu_used = round((total - idle) / total * 100, 1)

    return cpu_used

def parse_ram(raw_ram: str) -> dict:
    ram = {}
    lines = raw_ram.split('\n')

    for line in lines:
        if line.startswith('Mem:'):
            parts = line.split()
            ram['total'] = int(parts[1])
            ram['used'] = int(parts[2])
            ram['free'] = int(parts[3])
            ram['used_pct']  = round(ram['used'] / ram['total'] * 100, 1)
            break

    return ram

def build_result(host: str, raw: dict) -> dict:
    results = {
        'host':         host,
        'hostname':     raw['hostname'].strip(),
        'timestamp':    datetime.utcnow().isoformat() + 'Z',
        'cpu_used_pct': parse_cpu(raw['cpu']),
        'ram':          parse_ram(raw['ram']),
        'interfaces':   parse_interfaces(raw['ifconfig']),
    }

    return results