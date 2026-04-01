# Network & Infrastructure Monitor

A Python-based infrastructure monitoring system with a C++ network scanner.
Collects system metrics via SSH, exposes them through a REST API, and displays
them on a live web dashboard.

## Features

- SSH-based metric collection (CPU, RAM, network interfaces)
- Parallel monitoring of multiple hosts with thread-safe metric storage
- C++ subnet scanner with TCP port detection and multithreading
- REST API with Flask (`/api/*`)
- Live web dashboard (vanilla HTML/CSS/JS)
- Automatic metric refresh every 30 seconds
- Unit and integration tests (pytest)
- Docker support — no local dependencies required

## Architecture

```
[C++ Scanner] <-> [Python Collector] <-> [SSH Targets]
                        |
                   [Flask API /api/*]
                        |
              [Dashboard /] + [JSON endpoints]
```

## Tech Stack

- Python 3.11 — SSH automation, REST API, metric parsing
- C++ — subnet scanner (cross-platform, multithreading, Winsock2/POSIX)
- Netmiko — SSH connection handling
- Flask — REST API + frontend serving
- Docker — containerized build and deployment

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Web dashboard |
| `GET /api/metrics` | All monitored hosts (JSON) |
| `GET /api/metrics/<host>` | Single host metrics (JSON) |
| `GET /api/scan?subnet=10.0.1.&start=1&end=20` | Run network scan |
| `GET /api/health` | Service status |

## Quick Start

### Option 1 — Docker (recommended)

No dependencies required other than Docker.

```bash
git clone <repo>
cd <repo>
cp .env.example .env      # fill in your target hosts
docker compose up --build
```

Dashboard at `http://localhost:5000` — API at `http://localhost:5000/api/metrics`

### Option 2 — Local

**Requirements:** Python 3.11+, g++ compiler

```bash
git clone <repo>
cd <repo>
pip install -r requirements.txt
cp .env.example .env      # fill in your target hosts
```

Compile scanner — Windows:
```bash
cd scanner
g++ -o scanner.exe scanner.cpp -lws2_32 -pthread
cd ..
```

Compile scanner — Linux/Mac:
```bash
cd scanner
g++ -o scanner scanner.cpp -pthread
cd ..
```

Run:
```bash
python main.py
```

## Configuration

Copy `.env.example` to `.env` and fill in your values:

```env
TARGET_HOST_1=192.168.1.10
TARGET_USER_1=user
TARGET_PASS_1=password

SCAN_SUBNET=192.168.1.
SCAN_START=1
SCAN_END=20

INTERVAL_SECONDS=30
```

See `.env.example` for all available variables.

## Testing

```bash
pip install -r requirements-dev.txt
pytest tests/
```

Tests cover:
- Parser unit tests (CPU, RAM, interfaces)
- API endpoint tests (metrics, scan, health, 404 handling)
- SSH collector with mocked connections
- Thread safety of metric storage

## Project Structure

```
├── collector/
│   ├── ssh.py          # SSH connection and raw data collection
│   └── parser.py       # CPU, RAM, interface parsing
├── api/
│   └── app.py          # Flask REST API
├── scanner/
│   └── scanner.cpp     # C++ network scanner 
├── static/
│   ├── style.css
│   └── app.js
├── templates/
│   └── index.html      # Web dashboard
├── tests/
│   ├── test_parser.py
│   ├── test_api.py
│   └── test_ssh.py
├── .env.example
├── config.py
├── Dockerfile
├── docker-compose.yml
└── main.py
```
