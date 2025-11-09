# tradestation-api-python

<p align="center">
  <a href="https://github.com/santarsierilorenzo/tradestation-api-python/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/santarsierilorenzo/tradestation-api-python/ci.yml?style=flat-square" alt="CI/CD Pipeline"></a>
  <a href="https://coveralls.io/github/santarsierilorenzo/tradestation-api-python?branch=main"><img src="https://coveralls.io/repos/github/santarsierilorenzo/tradestation-api-python/badge.svg?branch=main" alt="Code Coverage"/></a>
  <a href="https://github.com/santarsierilorenzo/tradestation-api-python/releases"><img src="https://img.shields.io/github/v/release/santarsierilorenzo/tradestation-api-python?style=flat-square" alt="Latest Release"></a>
  <img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg?style=flat-square" alt="Platform">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Requests-007EC6?style=for-the-badge&logo=python&logoColor=white" alt="Requests">
  <img src="https://img.shields.io/badge/PyTest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="PyTest">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/ThreadPoolExecutor-FF9F00?style=for-the-badge&logo=python&logoColor=white" alt="ThreadPoolExecutor">
  <img src="https://img.shields.io/badge/Lock%20(Thread%20Safe)-C7253E?style=for-the-badge&logo=python&logoColor=white" alt="Thread Safety">
  <br>
  <img src="https://img.shields.io/badge/TradeStation%20API-002244?style=for-the-badge&logo=chartdotjs&logoColor=white" alt="TradeStation API">
  <img src="https://img.shields.io/badge/Streaming-1E90FF?style=for-the-badge&logo=websocket&logoColor=white" alt="Streaming">
  <img src="https://img.shields.io/badge/REST%20API-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="REST API">
  <img src="https://img.shields.io/badge/Multi--Threaded-FF6F00?style=for-the-badge&logo=python&logoColor=white" alt="Multi-threaded">
  <img src="https://img.shields.io/badge/DotEnv-4E9A06?style=for-the-badge&logo=dotenv&logoColor=white" alt="DotEnv">
</p>

<p align="center">
  <b>Fully Thread-Safe · Streaming Ready · Designed for Real-Time Trading</b><br>
  <i>Developed with ❤️ by Lorenzo Santarsieri · Built for TradeStation REST & Stream APIs</i>
</p>

> **tradestation-api-python** provides a complete Python SDK to simplify 
> interactions with the **TradeStation REST and Streaming APIs**.  
> It can be used both as a backend library in your trading systems or as a > base for custom automation projects.


## ⚠️ Read Before Continuing

**Disclaimer:**  
This is an **unofficial** package. Before using it, please make sure you fully understand the TradeStation API and its capabilities.  
This tool is provided *as-is* and is not affiliated with or endorsed by TradeStation Technologies, Inc.


## 🔐 Security Notice
Before using this package in production, **always** test your setup in a **simulated environment**.  
TradeStation APIs allow you to **place and modify real orders**, which can have financial consequences.  
Make sure you understand how this SDK and the underlying API work before executing any trades.

> 🧠 By default, the SDK runs in **SIM mode** (sandbox environment).  
> You can switch to **LIVE** mode by passing `use_sim=False` to the `TokenManager`.


## 🧩 Core Features
This SDK provides a robust and modular architecture built around:

### 🔑 Token Management (`auth.py`)
- Manages OAuth2 tokens (load, save, refresh).  
- Handles **race conditions** via a global thread lock.  
- Ensures safe concurrent token usage across threads.

### 💼 TradeStationClient (`client.py`)
Central entry point — automatically initializes and exposes:
1. `MarketDataAPI` for historical and live market data.
2. `MarketDataStream` for real-time market data streams.
3. `Brokerage` for managing accounts, balances, orders, and positions.
4. `BrokerStream` for real-time brokerage updates.

> 💡 The `TradeStationClient` ties together all services under a single, reusable interface.

### ⚙️ Base Classes
- `BaseAPIClient`: common HTTP request logic.  
- `BaseStreamClient`: handles WebSocket streaming, reconnects, and callbacks.

### 📡 Available Endpoints

#### `broker.py`
Manage brokerage operations:
```python
get_accounts()
get_balances()
get_balances_bod()
get_historical_orders()
get_historical_orders_by_id()
get_orders()
get_orders_by_id()
get_positions()
```

#### `mkt_data.py`
Handle historical and real-time market data:
```python
get_bars_between()
get_bars()
get_symbol_details()
get_crypto_symbol_names()
get_quote_snapshots()
```

#### `ts_stream.py`
Stream real-time market and brokerage events:
```python
stream_bars()
stream_quotes()
stream_market_depth_quotes()
stream_market_depth_aggregates()
stream_orders()
stream_orders_by_id()
stream_positions()
```

## ⚙️ Concurrency and Thread Safety

### 🧵 Token Management & Race Conditions
`TokenManager` uses a **class-level lock** (`threading.Lock`) ensuring that only one thread refreshes the token at a time.  
All other threads wait and reuse the refreshed token — avoiding race conditions and invalid credentials.

### ⚡ Multi-Threaded Historical Data Retrieval
`MarketDataAPI.get_bars_between()` automatically:
- Splits large date ranges into smaller API-compliant chunks.  
- Fetches data concurrently with `ThreadPoolExecutor`.  
- Merges and sorts all bars chronologically.

Example:
```python
from src.marketdata import get_bars_between

data = get_bars_between(
    token=token,
    symbol="MSFT",
    first_date="2023-01-01",
    last_date="2023-06-01",
    unit="Minute",
    interval=5,
    max_workers=10
)
```

✅ Benefits:
- Parallel network I/O for faster historical fetches.  
- Safe token reuse between threads.  
- Automatic chunking for TradeStation’s 57,600-bar limit.

## 📁 Project Structure

```bash
tradestation-api-python/
│
├── src/
│   ├── auth.py              # Token lifecycle manager
│   ├── base_client.py       # Base REST + stream client logic
│   ├── client.py            # Central TradeStationClient interface
│   ├── endpoints/
│   │   ├── broker.py        # Brokerage REST endpoints
│   │   ├── mkt_data.py      # Market Data REST endpoints
│   │   └── ts_stream.py     # Real-time streaming endpoints
│   └── __init__.py
│
├── test/                    # Unit test suite
│   ├── test_auth.py
│   ├── test_broker.py
│   ├── test_mkt_data.py
│   └── test_stream_base.py
│
├── examples/                # Example scripts
│   ├── get_market_data_example.py
│   └── stream_example.py
│
└── .env                     # Environment file for credentials
```

## 🧪 Testing and Coverage

Comprehensive `pytest` suite covers:
- REST endpoints (Brokerage & MarketData)
- HTTP error propagation and token refresh
- Thread-safety in token handling
- Streaming event handling and reconnection logic

Run the tests:
```bash
pytest -v
```

## 💡 Example Usage

```python
from src.client import TradeStationClient
from src.auth import TokenManager
from dotenv import load_dotenv

load_dotenv()
token_manager = TokenManager(use_sim=True)

ts_client = TradeStationClient(token_manager=token_manager)

data = ts_client.market_data.get_bars_between(
    symbol="AAPL",
    first_date="2025-01-01",
    interval=1,
    unit="Minute",
    max_workers=15,
)
```

## 🧰 Development Setup (Docker + Dev Containers)

### Requirements
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [VS Code](https://code.visualstudio.com/)
- [Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Setup
```bash
git clone https://github.com/santarsierilorenzo/tradestation-api-python
code tradestation-api-python
```

Then open **Command Palette →**  
`Dev Containers: Rebuild Without Cache and Reopen in Container`

✅ This builds a reproducible containerized environment and runs `setup.sh`, marking untracked files (like `.devcontainer/`) as unchanged for a clean workspace.

## 🪪 License
MIT © 2025 | Developed with ❤️ by Lorenzo Santarsieri
