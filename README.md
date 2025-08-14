# 🔋 Grid Optimization System

**Intelligent Power Grid Management with AI Agents**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![NVIDIA NAT](https://img.shields.io/badge/NVIDIA-NeMo%20Agent%20Toolkit-76B900.svg)](https://github.com/NVIDIA/NeMo-Agent-Toolkit)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## 📖 Overview

**GridOpt** is a power grid optimization system that leverages AI agents powered by **NVIDIA NeMo Agent Toolkit (NAT)** to deliver:

- 🔄 **Autonomous grid optimization** with minimal human intervention
- 📊 **Real-time monitoring** and predictive analytics
- 🤖 **Multi-agent coordination** for complex decision-making  
- 🔒 **Enterprise-grade security** with role-based access control
- 📈 **Scalable architecture** supporting multiple grid regions

## 📁 Project Structure

```
grid_optimization/                 # Production-ready structure
├── src/
│   ├── grid_core/               # Core grid optimization
│   │   ├── __init__.py
│   │   ├── db.py                # Database operations
│   │   ├── security.py          # Access control
│   │   └── tools/               # Grid utilities
│   └── nat_toolkit/             # NVIDIA NAT integration
│       ├── register_simple.py   # NAT functions
│       └── configs/             # Agent configurations
├── configs/                     # Main configuration files
├── tests/                       # Test suite
├── deployment/                  # Docker deployment
├── test_core.py                 # System test
└── pyproject.toml              # Project configuration
```

## 🔧 Installation

### Prerequisites

- **Python 3.11+** (NAT compatibility)
- **NVIDIA API Key** (optional, for NIM models)
- **OpenAI API Key** (optional, for GPT models)

### Quick Start

```bash
# Set up environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e .

# Initialize database
python -c "from src.grid_core.db import init_db; init_db()"

# Test installation
python test_core.py
```

### 🐳 Docker Deployment

```bash
# Quick start with Docker Compose
docker-compose -f deployment/docker-compose.yml up --build

# Production mode
docker-compose -f deployment/docker-compose.yml up -d
```

## 🤖 NAT Usage

### Command Line Interface

```bash
# Install NVIDIA NeMo Agent Toolkit
uv pip install aiqtoolkit

# Basic grid optimization
aiq run --config_file configs/workflow.yml \
        --input "Optimize the grid for region us-west"

# Advanced reasoning analysis
aiq run --config_file src/nat_toolkit/configs/config-reasoning.yml \
        --input "Analyze efficiency trends and recommend optimization strategy"

# Using NVIDIA NIM models
export NVIDIA_API_KEY="your-nvidia-key"
aiq run --config_file configs/workflow.yml \
        --input "Show grid status for all regions" \
        --llm nim_llm
```

### REST API

```bash
# Start the server
python server.py

# Health check
curl http://localhost:8000/health

# AI agent query
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"input": "Optimize the grid to minimize losses"}'

# Interactive API docs
open http://localhost:8000/docs
```

### Example Interactions

**Grid Optimization:**
```
> "Optimize the grid for region us-west to minimize power losses"

Grid Optimization Complete for US-WEST:
✅ Status: success
📊 Power Loss Reduction: 12.5%
⚡ Optimal Configuration: Transformer #3 voltage +2%
💰 Cost Savings: $45,000
🕒 Optimization Time: 3.2s
```

**Performance Analysis:**
```
> "Analyze efficiency trends for the eastern grid"

Grid Efficiency Analysis for US-EAST:
📈 Current Efficiency: 94.2%
📊 Average Efficiency: 91.8%
📉 Trend: Improving
🎯 Target Efficiency: 95%
💡 Status: Excellent Performance
```

## ⚙️ Configuration

### Environment Variables

```bash
# API Keys
export OPENAI_API_KEY="your-openai-key"
export NVIDIA_API_KEY="your-nvidia-key"

# Database
export DATABASE_URL="sqlite:///gridopt.db"

# Server Configuration
export GRID_SERVER_HOST="0.0.0.0"
export GRID_SERVER_PORT="8000"
```

### Agent Configuration

**Basic React Agent** (`configs/workflow.yml`):
```yaml
llms:
  grid_llm:
    _type: openai
    model_name: gpt-4o
    max_tokens: 4096
    temperature: 0.1

workflow:
  _type: react_agent
  tool_names:
    - grid_optimize
    - grid_status
    - grid_analyze
  llm_name: grid_llm
  max_iterations: 8
```

## 📊 NAT Tool Functions

### `grid_optimize(region: str)`
Optimizes power grid configuration for specified region.
- Minimizes power losses and improves efficiency
- Provides cost savings analysis and configuration recommendations
- Includes safety validation and regulatory compliance

### `grid_status(region: str)`
Retrieves current operational status and performance metrics.
- Real-time load, capacity, and efficiency data
- Active alerts and maintenance schedules
- Historical optimization results

### `grid_analyze(region: str, metric: str)`
Performs detailed analysis of grid performance metrics.
- Trend analysis for efficiency, load, and capacity
- Comparative analysis across time periods
- Predictive insights and optimization recommendations

## 🧪 Testing

### System Test

```bash
# Comprehensive system test (recommended first step)
python test_core.py

# Expected output:
# ✅ Core modules imported successfully
# ✅ Security functions working correctly  
# ✅ Database operations functional
# ✅ Grid optimization working
# ✅ Project structure complete
```

### Component Testing

```bash
# Test individual components
python -c "from src.grid_core import optimize_grid; print(optimize_grid('test-region'))"

# Test async NAT functions
python -c "
import asyncio
from src.nat_toolkit.register_simple import optimize_grid_region
result = asyncio.run(optimize_grid_region('test-region'))
print('Async optimization:', result['status'])
"

# Test security functions
python -c "
from src.grid_core.security import validate_region_access, sanitize_region_name
print('Valid region test:', validate_region_access('us-west'))
print('Sanitization test:', sanitize_region_name('Test@Region!'))
"
```

## 🚀 Production Deployment

### Deployment Options

| Method | Use Case | Commands |
|--------|----------|----------|
| **Docker Compose** | Single server | `make docker-run` |
| **Manual Install** | Custom environments | `make install && make run` |
| **Development** | Local development | `make run-dev` |

### Production Checklist

```bash
# 1. Environment setup
export DATABASE_URL="postgresql://user:pass@localhost/gridopt"
export OPENAI_API_KEY="your-openai-key"
export GRID_SERVER_HOST="0.0.0.0" 
export GRID_SERVER_PORT="8000"

# 2. Database initialization
make init-db

# 3. Run production server
docker-compose -f deployment/docker-compose.yml up -d

# 4. Health verification
curl http://localhost:8000/health
```

## 📚 Quick Commands Reference

### Setup Commands

```bash
# Setup and Testing (Production Ready)
python -m venv .venv && source .venv/bin/activate
uv pip install -e .
python -c "from src.grid_core.db import init_db; init_db()"
python test_core.py                    # Complete system test

# Component Testing
python -c "from src.grid_core import optimize_grid; print(optimize_grid('test'))"
python -c "from src.grid_core.security import validate_region_access; print(validate_region_access('us-west'))"
```

### NAT Commands

```bash
# Modern functions
aiq run --config_file configs/workflow.yml --input "Use grid_optimize for us-west region"
aiq run --config_file configs/workflow.yml --input "Show grid_status for all regions"

# Reasoning agent
aiq run --config_file src/nat_toolkit/configs/config-reasoning.yml --input "Analyze trends"

# NVIDIA NIM models
export NVIDIA_API_KEY="your-key"
aiq run --config_file configs/workflow.yml --input "Optimize with NVIDIA models" --llm nim_llm
```

### Docker Commands

```bash
# Docker deployment
docker-compose -f deployment/docker-compose.yml up --build
docker-compose -f deployment/docker-compose.yml up -d  # Production mode
```

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NVIDIA NeMo Agent Toolkit** - Core AI agent framework
- **FastAPI** - High-performance web framework
- **SQLAlchemy** - Database ORM and management
- **OpenAI** - Language model APIs
- **NVIDIA NIM** - High-performance model inference

---

<div align="center">

**🔋 Built with ❤️ for intelligent power grid management**

*Powered by NVIDIA NeMo Agent Toolkit • FastAPI • Python 3.11+*

</div>