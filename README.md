# Network & Infrastructure Monitor

A Python-based infrastructure monitoring system with a C++ network scanner.
Collects system metrics via SSH and exposes them through a REST API.

## Features

- SSH-based metric collection (CPU, RAM, network interfaces)
- Parallel monitoring of multiple hosts
- C++ subnet scanner with TCP port detection
- REST API with Flask
- Automatic metric refresh every 30 seconds
- Docker support - no local dependencies required

## Architecture

```
[C++ Scanner] <-> [Python Collector] <-> [SSH Targets]
                        |
                   [Flask API]
                        |
                 [JSON / /metrics]
```

## Tech Stack

- Python 3.11 - SSH automation, REST API, metric parsing
- C++ - subnet scanner (cross-platform, multithreading)
- Netmiko - SSH connection handling
- Flask - REST API
- Docker - containerized build and deployment

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /metrics` | All monitored hosts |
| `GET /metrics/<host>` | Single host metrics |
| `GET /scan?subnet=10.0.1.&start=1&end=20` | Run network scan |
| `GET /health` | Service status |

## Quick Start

### Option 1 — Docker (recommended)

No dependencies required other than Docker.

```bash
git clone <repo>
cd <repo>
docker compose up --build
```

API available at `http://localhost:5000/metrics`

### Option 2 — Local

**Requirements:** Python 3.11+, g++ compiler

```bash
git clone <repo>
cd <repo>
pip install -r requirements.txt
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

API available at `http://localhost:5000/metrics`

## Configuration

Set target hosts via environment variables or edit `config.py` directly:

```env
TARGET_HOST_1=10.0.1.99
TARGET_USER=user
TARGET_PASS=user
```

## Project Structure

```
├── collector/
│   ├── ssh.py       # SSH connection and raw data collection
│   └── parser.py    # CPU, RAM, interface parsing
├── api/
│   └── app.py       # Flask REST API
├── scanner/
│   └── scanner.cpp  # C++ network scanner (cross-platform)
├── config.py        # Configuration
├── Dockerfile
├── docker-compose.yml
└── main.py          # Entry point
```
