from collector.parser import parse_interfaces, parse_cpu, parse_ram, build_result

def test_parse_interfaces():
    raw = """eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
    inet 192.168.1.10  netmask 255.255.255.0  broadcast 192.168.1.255
    ether 00:11:22:33:44:55"""
    
    result = parse_interfaces(raw)
    assert "eth0:" in result
    assert result["eth0:"]["ip_address"] == "192.168.1.10"
    assert result["eth0:"]["mac_address"] == "00:11:22:33:44:55"

def test_parse_cpu():
    raw = "cpu  12345 100 200 3000 4000 500 0 0 0 0" 
    assert parse_cpu(raw) == 80.8  

def test_parse_ram():
    raw = """Mem:  16384  8192  8192   0   0   0"""
    result = parse_ram(raw)
    assert result["total"] == 16384
    assert result["used"] == 8192
    assert result["free"] == 8192
    assert result["used_pct"] == 50.0

def test_build_result():
    raw = {
        "hostname": "test-host",
        "cpu": "cpu  1000 0 0 9000 0 0 0 0 0 0",
        "ram": "Mem:  16384  8192  8192",
        "ifconfig": "eth0: ... inet 192.168.1.10 ... ether 00:11:22:33:44:55"
    }
    result = build_result("192.168.1.10", raw)
    assert result["host"] == "192.168.1.10"
    assert result["hostname"] == "test-host"
    assert "cpu_used_pct" in result
    assert "ram" in result
    assert "interfaces" in result