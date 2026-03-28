from netmiko import ConnectHandler
import json

device = {
    'device_type': 'linux',
    'host': '10.0.1.99',
    'username': 'user',
    'password': 'user'
}

connection = ConnectHandler(**device)

output = connection.send_command('ifconfig')

connection.disconnect()

interfaces = {}

lines = output.split('\n')

current_interface = None

for line in lines:
    if line and not line.startswith(' '):
        current_interface = line.split()[0]
        interfaces[current_interface] = {}
    elif current_interface:
        if 'inet ' in line:
            interfaces[current_interface]['ip_address'] = line.split()[1]
        elif 'ether ' in line:
            interfaces[current_interface]['mac_address'] = line.split()[1]

print(interfaces)

with open('interfaces.json', 'w') as f:
    json.dump(interfaces, f, indent=4)