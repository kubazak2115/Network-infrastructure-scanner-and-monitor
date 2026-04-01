import os

DEVICES = [
    {
        'device_type': 'linux',
        'host':     os.getenv('TARGET_HOST_1', '192.168.1.1'),
        'username': os.getenv('TARGET_USER_1', 'user'),
        'password': os.getenv('TARGET_PASS_1', 'password'),
    },
    {
        'device_type': 'linux',
        'host':     os.getenv('TARGET_HOST_2', '192.168.1.2'),
        'username': os.getenv('TARGET_USER_2', 'user'),
        'password': os.getenv('TARGET_PASS_2', 'password'),
    },
]

API_HOST = '0.0.0.0'
API_PORT = 5000

INTERVAL_SECONDS = 30

# default scanner setting - can be overridden by env vars
SCAN_SUBNET = os.getenv('SCAN_SUBNET', '192.168.1.')
SCAN_START  = int(os.getenv('SCAN_START', '1'))
SCAN_END    = int(os.getenv('SCAN_END', '20'))