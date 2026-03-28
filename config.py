import os

DEVICE = {
    'device_type': 'linux',
    'host':        os.getenv('TARGET_HOST', '10.0.1.99'),
    'username':    os.getenv('TARGET_USER', 'user'),
    'password':    os.getenv('TARGET_PASS', 'user'),
}

API_HOST = '0.0.0.0'
API_PORT = 5000