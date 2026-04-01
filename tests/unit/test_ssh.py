from unittest.mock import patch, MagicMock
from collector.ssh import collect_raw, run_scanner
import json

@patch('collector.ssh.ConnectHandler')
def test_collect_raw(mock_connect):
    mock_conn = MagicMock()
    mock_conn.send_command.side_effect = [
        "ifconfig output",          
        "cpu  1000 0 0 9000",       
        "Mem: 16384 8192 8192",     
        "test-host"                 
    ]
    mock_connect.return_value = mock_conn

    device = {'device_type': 'linux', 'host': '1.2.3.4', 'username': 'u', 'password': 'p'}
    result = collect_raw(device)

    assert result['hostname'] == 'test-host'
    assert 'ifconfig' in result
    mock_conn.disconnect.assert_called_once()

@patch('collector.ssh.subprocess.run')
@patch('collector.ssh.platform.system', return_value='Linux')
def test_run_scanner(mock_system, mock_run):
    mock_run.return_value.stdout = 'some lines\n[{"ip": "192.168.1.10", "alive": true, "ports": [22]}]\n'
    result = run_scanner("192.168.1.", 1, 20)
    assert len(result) == 1
    assert result[0]["ip"] == "192.168.1.10"