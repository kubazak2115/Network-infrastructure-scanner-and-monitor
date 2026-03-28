from netmiko import ConnectHandler
import json
from datetime import datetime

device = {
    'device_type': 'linux',
    'host': '10.0.1.99',
    'username': 'user',
    'password': 'user'
}

connection = ConnectHandler(**device)

# data collection using linux commands
raw_ifconfig  = connection.send_command('ifconfig')
raw_cpu       = connection.send_command('cat /proc/stat | grep "cpu" | head -n 1')
raw_ram       = connection.send_command('free -m')
raw_hostname  = connection.send_command('hostname')

connection.disconnect()

# parsing the interfaces data
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


#parsing the cpu data
cpu_values = raw_cpu.split()
user   = int(cpu_values[1])
nice   = int(cpu_values[2])
system = int(cpu_values[3])
idle   = int(cpu_values[4])

total = user + nice + system + idle
cpu_used = round((total - idle) / total * 100, 1)

#parsing the ram data
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

#results
results = {
    'host': device['host'],
    'hostname': raw_hostname,
    'timestamp':  datetime.utcnow().isoformat() + 'Z',
    'cpu_used_pct': cpu_used,
    'ram': ram,
    'interfaces': interfaces
}

print(json.dumps(results, indent=4))

with open('metrics.json', 'w') as f:
    json.dump(results, f, indent=4)