# Viewer Bot

Playwright-based automated web page visitor bot

![Demo](.data/demo.png)

## Installation

```bash
poetry install
poetry run playwright install firefox
```

## Proxy Setup

If you want to use the `--use-proxy` option, you need to set up Tor.

### Install Tor

```bash
# macOS
brew install tor

# Ubuntu/Debian
sudo apt-get install tor

# Other platforms
# Visit https://www.torproject.org/download/
```

### Run Tor

When using `--use-proxy`, you need to run Tor with multiple SOCKS ports.
The number of ports should match `--concurrency` value.

#### Using the provided script (recommended)

```bash
# Start Tor with 5 ports (9050-9054)
./start_tor.sh 5

# Start Tor with 10 ports starting from 9050
./start_tor.sh 10

# Start Tor with 3 ports starting from 9100
./start_tor.sh 3 9100

# Stop Tor
./stop_tor.sh
```

**Script Parameters:**

- First argument: Number of ports (default: `5`)
- Second argument: Starting port number (default: `9050`)

#### Manual execution

```bash
# For concurrency=5, run ports 9050-9054
tor --SocksPort 9050 --SocksPort 9051 --SocksPort 9052 --SocksPort 9053 --SocksPort 9054
```

## Usage

### Basic Execution

```bash
poetry run python bot.py
```

### With Options

```bash
poetry run python bot.py --url "https://example.com" --concurrency 5 --headless --use-proxy
```

**Parameters**

- `--url`: URL to visit (default: `https://httpbin.org/ip`)
- `--concurrency`: Number of concurrent bots (default: `5`)
- `--headless`: Headless mode (default: `True`)
- `--use-proxy`: Whether to use proxy (default: `True`)

## ⚠️ Disclaimer

**This project is for educational and testing purposes only.**

This bot is designed to help you learn about:

- Web automation using Playwright
- Browser fingerprinting and anti-detection techniques
- Proxy rotation and network programming
- Asynchronous Python programming

**Important:**

- Only use this bot to test
- Do not use this to artificially inflate traffic metrics or manipulate analytics
- Be aware that automated traffic generation may violate platform policies

The authors assume no responsibility for misuse of this software.
