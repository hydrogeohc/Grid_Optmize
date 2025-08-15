# Grid Optimization System

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-311/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#testing)
[![NAT Integration](https://img.shields.io/badge/NAT%20integration-✅%20working-brightgreen.svg)](#nat-toolkit-integration)
[![Code Style](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/psf/black)

A **professional AI-powered grid optimization platform** with **NVIDIA NeMo Agent Toolkit (NAT) integration**. Features real-time power grid optimization, multi-region support, and advanced analytics capabilities.

---

## ✨ Key Features

- 🔋 **Real-time Grid Optimization**: SciPy-based algorithms for power supply/demand balancing
- 🌍 **Multi-Region Support**: US-West, US-East, US-Central, and PG&E regions
- 🤖 **NAT Integration**: NVIDIA NeMo Agent Toolkit for AI-powered operations  
- 🚀 **High Performance**: Sub-millisecond optimization times
- 📊 **Professional API**: FastAPI-based REST endpoints with async support
- 🔧 **Modern CLI**: Clean command-line interface with multiple workflows
- 📈 **Database Integration**: SQLite-based persistence with SQLAlchemy ORM
- ✅ **Production Ready**: Comprehensive test coverage and clean codebase

---

## 🏗️ Architecture

```
Grid_Optimize/
├── grid_optimization/           # 🎯 Main Package
│   ├── core/                   # Core optimization engine
│   │   ├── operations.py       # Grid optimization algorithms (SciPy)
│   │   ├── database.py         # Database models & operations
│   │   ├── models.py           # Pydantic data models
│   │   └── initialization.py   # Database initialization
│   ├── integrations/           # External integrations
│   │   ├── nat/               # NAT toolkit integration
│   │   │   └── register.py     # AIQ function registration
│   │   └── aiq_integration.py  # AIQ configuration helpers
│   ├── api/                    # REST API
│   │   ├── server.py           # FastAPI application
│   │   └── routes/             # API endpoints
│   │       ├── grid.py         # Grid operations
│   │       └── health.py       # Health checks & diagnostics
│   ├── cli/                    # Command line interface
│   │   └── commands.py         # CLI commands
│   └── utils/                  # Shared utilities
│       ├── config.py           # Configuration management
│       └── logging.py          # Logging setup
├── configs/                    # Configuration files
│   ├── aiq/                   # AIQ-specific configs
│   │   ├── basic.yml           # Basic AIQ setup
│   │   ├── full.yml            # Full feature set
│   │   └── no_llm.yml          # No LLM dependencies
│   └── app.yml                # Application configuration
├── tests/                      # Comprehensive test suite
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   └── fixtures/              # Test data
└── deployment/                 # Deployment utilities
    ├── Dockerfile             # Container setup
    └── docker-compose.yml     # Multi-service deployment
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone and install
git clone <repository-url>
cd Grid_Optimize

# Install with dependencies
pip install -e .

# Initialize database
python -c "from grid_optimization.core.initialization import init_test_data; init_test_data()"

# Verify installation
grid-optimize --help
```

### Basic Usage

#### 1. Command Line Interface
```bash
# Optimize a specific region
grid-optimize optimize us-west

# Check optimization status
grid-optimize status us-west

# Interactive mode
grid-optimize interactive

# Test all functionality
grid-optimize test
```

#### 2. Python API
```python
import grid_optimization.core.operations as ops

# Direct optimization
result = ops.optimize_grid('us-west')
print(f"Optimized Supply: {result['optimized_supply']:.2f} MW")
print(f"Power Losses: {result['losses']:.2e} MW²")

# Get latest results
latest = ops.get_latest_optimization('us-west')
print(f"Timestamp: {latest['timestamp']}")
```

#### 3. Async NAT Functions
```python
import asyncio
from grid_optimization.integrations.nat.register import optimize_grid_region

async def optimize():
    result = await optimize_grid_region('us-west')
    print(f"Status: {result['status']}")
    print(f"Region: {result['region']}")
    
asyncio.run(optimize())
```

#### 4. REST API
```bash
# Start the API server
grid-server

# Use the API
curl -X POST "http://localhost:8000/grid/optimize" \
     -H "Content-Type: application/json" \
     -d '{"region": "us-west"}'

# Health check
curl http://localhost:8000/health
```

---

## 🤖 NVIDIA NAT Integration

Full **NVIDIA NeMo Agent Toolkit (NAT)** integration for AI-powered operations.

### Features
- ✅ **AIQ Compatible**: Functions discoverable via entry points
- ✅ **Async Support**: Non-blocking operations for better performance
- ✅ **Multi-Region**: All grid regions supported (us-west, us-east, us-central, pgae)
- ✅ **Error Handling**: Robust error management and logging
- ✅ **Production Ready**: Clean, tested, and optimized code

### Available NAT Functions
| Function | Description | Return Type |
|----------|-------------|-------------|
| `optimize_grid_region(region)` | Optimize power grid for specified region | `dict` |
| `get_optimization_status(region)` | Get current optimization status | `dict` |
| `analyze_grid_metrics(region)` | Analyze grid performance metrics | `dict` |

### AIQ Usage
```bash
# Set OpenAI API key (for LLM features)
export OPENAI_API_KEY="your-api-key-here"

# Run with AIQ
aiq run --config_file configs/aiq/basic.yml --input "Optimize grid for us-west region"

# No-LLM mode (direct function calls)
aiq run --config_file configs/aiq/no_llm.yml
```

---

## 📊 Testing & Quality

### Test Results
- ✅ **Core Functions**: All grid optimization algorithms working
- ✅ **NAT Integration**: All async functions operational
- ✅ **Database Operations**: SQLite persistence working
- ✅ **API Endpoints**: FastAPI routes responding correctly
- ✅ **Entry Points**: AIQ discovery working

### Code Quality
- ✅ **Formatted**: Black code formatter (line length 100)
- ✅ **Import Sorted**: isort with black profile
- ✅ **Linting**: flake8 compliant (main codebase)
- ✅ **Type Hints**: Modern Python typing throughout
- ✅ **Documentation**: Comprehensive docstrings

### Run Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Test specific components
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v

# Test NAT integration
python -c "from grid_optimization.integrations.nat.register import optimize_grid_region; import asyncio; print(asyncio.run(optimize_grid_region('us-west')))"

# Verify AIQ entry points
python -c "import pkg_resources; print([ep.name for ep in pkg_resources.iter_entry_points('aiq.components') if 'nat_toolkit' in ep.name])"
```

---

## 📋 API Reference

### Grid Optimization Endpoints

#### POST `/grid/optimize`
Optimize power grid for a specific region.

**Request:**
```json
{
  "region": "us-west",
  "parameters": {}  // optional
}
```

**Response:**
```json
{
  "region": "us-west",
  "optimized_supply": 1010.00,
  "optimized_demand": 1010.00, 
  "losses": 4.57e-12,
  "timestamp": "2025-08-15T10:30:00Z"
}
```

#### GET `/grid/status/{region}`
Get current grid status and optimization history.

#### GET `/grid/regions`
List all available regions.

### Health Endpoints

#### GET `/health`
Comprehensive system health check.

#### GET `/ready` / GET `/live`
Kubernetes-style readiness and liveness probes.

### Available Regions
- `us-west` - Western United States  
- `us-east` - Eastern United States
- `us-central` - Central United States
- `pgae` - Pacific Gas & Electric

---

## ⚙️ Configuration

### Application Settings (`configs/app.yml`)
```yaml
environment: development
debug: true
log_level: INFO

database:
  type: sqlite
  path: gridopt.db

api:
  host: 127.0.0.1
  port: 8000

grid:
  default_region: us-west
  max_iterations: 100
  tolerance: 1e-6
```

### AIQ Configuration (`configs/aiq/basic.yml`)
```yaml
general:
  use_uvloop: true

llms:
  grid_llm:
    _type: openai
    model_name: gpt-4o-mini
    temperature: 0.1

functions:
  optimize_grid:
    _type: optimize_grid
  show_last_optimization:
    _type: show_last_optimization

workflow:
  _type: react_agent
  tool_names:
    - optimize_grid
    - show_last_optimization
  llm_name: grid_llm
```

---

## 🛠️ Development

### Code Standards
- **Python 3.11+**: Modern Python features and performance
- **Black Formatting**: 100-character line length
- **Type Hints**: Comprehensive typing throughout
- **SQLAlchemy ORM**: Database operations and migrations
- **FastAPI**: Modern async web framework
- **Pydantic**: Data validation and serialization

### Adding New Regions
1. Update database initialization in `core/initialization.py`
2. Add region to `AVAILABLE_REGIONS` in models
3. Update configuration files
4. Add comprehensive tests

### Extending NAT Integration
1. Add functions to `integrations/nat/register.py`
2. Register entry points in `pyproject.toml`
3. Update AIQ configurations
4. Add unit and integration tests

### Contributing
1. Fork the repository
2. Create a feature branch
3. Follow code standards (black, isort, flake8)
4. Add comprehensive tests
5. Submit a pull request

---

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Support

- **Documentation**: Comprehensive inline documentation and examples
- **Testing**: Run the test suite to verify functionality
- **Issues**: Please report with detailed reproduction steps

---

**Built with ❤️ using Python, FastAPI, SciPy, SQLAlchemy, and NVIDIA NAT**