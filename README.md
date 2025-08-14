# 🔋 Grid Optimization System

**Intelligent Power Grid Management with AI Agents**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![NVIDIA NAT](https://img.shields.io/badge/NVIDIA-NeMo%20Agent%20Toolkit-76B900.svg)](https://github.com/NVIDIA/NeMo-Agent-Toolkit)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-00D7FF.svg)](https://fastapi.tiangolo.com/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 📖 Overview

**GridOpt** is a state-of-the-art power grid optimization system that leverages AI agents to revolutionize energy management. By integrating the **NVIDIA NeMo Agent Toolkit (NAT)** with advanced optimization algorithms, it delivers:

- 🔄 **Autonomous grid optimization** with minimal human intervention
- 📊 **Real-time monitoring** and predictive analytics
- 🤖 **Multi-agent coordination** for complex decision-making  
- 🔒 **Enterprise-grade security** with role-based access control
- 📈 **Scalable architecture** supporting multiple grid regions

## 🚀 Key Features

### 🤖 **AI Agent Capabilities**
- **React Agent**: Fast, responsive optimization decisions
- **Reasoning Agent**: Complex analysis with step-by-step reasoning
- **Multi-Model Support**: OpenAI GPT, NVIDIA NIM, and custom models
- **Custom Tools**: Grid-specific functions for optimization, monitoring, and analysis

### ⚡ **Grid Operations**
- **Real-time Optimization**: Minimize power losses and improve efficiency
- **Multi-Region Management**: Handle multiple grid regions simultaneously
- **Predictive Analysis**: Trend analysis and performance forecasting
- **Load Balancing**: Dynamic load distribution and capacity optimization

### 🛡️ **Security & Reliability**
- **Access Control**: Role-based security with region validation
- **Safety Guardrails**: Automated safety checks and regulatory compliance
- **Fault Tolerance**: Robust error handling and fallback mechanisms
- **Audit Logging**: Comprehensive logging for compliance and debugging

## 📁 Project Structure

### ✨ Clean Production Structure (Recommended)

**Location**: `Grid_optimization_clean/grid_optimization/`

```
grid_optimization/                 # ✅ Production-ready directory
├── src/                          # Source code
│   ├── grid_core/               # Core grid optimization
│   │   ├── __init__.py          # Main module exports
│   │   ├── db.py                # Database operations & models
│   │   ├── security.py          # Security validation & access control
│   │   └── tools/               # Grid-specific utilities
│   └── nat_toolkit/             # NVIDIA NAT integration
│       ├── __init__.py          # NAT module initialization
│       ├── register_simple.py   # Simplified NAT registration
│       ├── README.md            # NAT toolkit documentation
│       └── configs/             # Agent configurations
├── configs/                     # Main configuration files
├── tests/                       # Test suite
├── deployment/                  # Docker & deployment
├── test_core.py                 # ✅ Comprehensive system test
├── pyproject.toml              # Python project configuration
└── README.md                   # This file
```

**Features**: ✅ Self-contained • ✅ Clean imports • ✅ Production ready • ✅ Full test coverage

### 📂 Original Development Structure

**Location**: `Grid_optimization/` (root directory)

```
Grid_optimization/
├── grid_optimization/           # Main package directory
│   ├── src/                    # Source code
│   │   ├── grid_core/         # Core optimization logic
│   │   └── nat_toolkit/       # NAT integration with register.py
│   ├── aiqtoolkit/            # Local NAT toolkit installation
│   ├── configs/               # Configuration files
│   ├── deployment/            # Docker and deployment files
│   └── tests/                 # Test suite
├── Grid_optimization_clean/    # Clean version (production)
├── server.py                  # FastAPI development server
├── deploy.py                  # Deployment utilities
└── usage_examples.py          # Usage demonstrations
```

**Features**: 🔧 Full NAT toolkit • 🔄 Legacy compatibility • 🚀 All integrations available

### 🎯 Choose Your Version

| Version | Use Case | Location | Quick Test |
|---------|----------|----------|------------|
| **Clean** | Production deployment | `Grid_optimization_clean/grid_optimization/` | `python test_core.py` |
| **Original** | Development & NAT integration | `Grid_optimization/` | `python usage_examples.py` |

## 🔧 Installation

### Prerequisites

| Requirement | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11+ | Core runtime (NAT compatibility) |
| **Git** | Latest | Version control |
| **Docker** | 20.0+ | Containerized deployment (optional) |
| **NVIDIA API Key** | - | NIM model access (optional) |
| **OpenAI API Key** | - | GPT model access (optional) |

### Quick Start

#### ✨ Clean Version (Production Ready)

```bash
# 1. Navigate to clean structure
cd Grid_optimization_clean/grid_optimization

# 2. Set up Python environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -e .

# 4. Initialize database
python -c "from src.grid_core.db import init_db; init_db()"

# 5. Test the installation
python test_core.py

# Expected output:
# ✅ Core modules imported successfully
# ✅ Security functions working correctly
# ✅ Database operations functional
# ✅ Grid optimization working
# ✅ Project structure complete
```

#### 📂 Original Version (Full NAT Integration)

```bash
# 1. Navigate to original structure
cd Grid_optimization

# 2. Set up Python environment (if needed)
python -m venv .venv
source .venv/bin/activate

# 3. Install with NAT toolkit
pip install -e ".[dev]"

# 4. Test with usage examples
python usage_examples.py

# 5. Run NAT integration (requires aiqtoolkit)
aiq run --config_file configs/workflow.yml \
        --input "Test grid optimization for us-west"
```

The application will be available at **http://localhost:8000** with interactive API docs at **http://localhost:8000/docs**.

### 🐳 Docker Deployment

```bash
# Quick start with Docker Compose
make docker-run

# Or manually
docker-compose -f deployment/docker-compose.yml up --build

# Production deployment
docker-compose -f deployment/docker-compose.yml up -d

# Stop services
make docker-stop
```

**Services included:**
- **Grid API Server** - Main application (port 8000)
- **Database** - SQLite with persistent storage
- **Health Monitoring** - Built-in health checks

## 🤖 Usage

### 🤖 AI Agent Interface

#### Command Line (With NAT Installation)

```bash
# Install NVIDIA NeMo Agent Toolkit first
# pip install aiqtoolkit

# Unified NAT toolkit usage
aiq run --config_file configs/workflow.yml \
        --input "Optimize the grid for region us-west"

# Advanced reasoning for complex scenarios  
aiq run --config_file src/nat_toolkit/configs/config-reasoning.yml \
        --input "Analyze efficiency trends and recommend optimization strategy"

# Using unified configuration with all functions
aiq run --config_file src/nat_toolkit/configs/unified-config.yml \
        --input "Show comprehensive grid analysis for all regions"

# Using NVIDIA NIM models (requires API key)
export NVIDIA_API_KEY="your-nvidia-key"
aiq run --config_file configs/workflow.yml \
        --input "Show grid status for all regions" \
        --llm nim_llm
```

#### 🧪 Development Testing (No NAT Required)

```bash
# Test core functionality
python test_core.py

# Test individual components
python -c "from src.grid_core import optimize_grid; print(optimize_grid('test-region'))"

# Test NAT integration components
python -c "from src.nat_toolkit.register_simple import optimize_grid_region; import asyncio; print(asyncio.run(optimize_grid_region('test-region')))"
```

#### 🌐 REST API

```bash
# Health check
curl http://localhost:8000/health

# AI agent query
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"input": "Optimize the grid to minimize losses"}'

# Region-specific optimization
curl -X POST "http://localhost:8000/optimize/us-west" \
     -H "Content-Type: application/json"

# Status monitoring  
curl "http://localhost:8000/status/us-west"

# Interactive API documentation
open http://localhost:8000/docs
```

### Interactive Examples

**Grid Optimization:**
```
> "Optimize the grid for region us-west to minimize power losses"

Grid Optimization Complete for US-WEST:
✅ Status: success
📊 Power Loss Reduction: 12.5%
⚡ Optimal Configuration: Transformer #3 voltage +2%, Switch S-15 rerouted
💰 Cost Savings: $45,000
🕒 Optimization Time: 3.2s
🔧 Next Maintenance: 2024-09-15
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
📊 Data Points: 24 readings analyzed
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

**Advanced Reasoning** (`configs/workflow-reasoning.yml`):
```yaml
workflow:
  _type: reasoning_agent
  reasoning_model_name: analysis_llm
  max_iterations: 12
  # Enhanced reasoning for complex scenarios
```

## 🧪 Testing

### ✨ Clean Version Testing

#### 🚀 Quick System Test

```bash
# Navigate to clean structure
cd Grid_optimization_clean/grid_optimization

# Comprehensive system test (recommended first step)
python test_core.py

# Expected output:
# ✅ Core modules imported successfully
# ✅ Security functions working correctly  
# ✅ Database operations functional
# ✅ Grid optimization working
# ✅ Configuration files valid
# ✅ Project structure complete
```

#### 🔬 Detailed Clean Testing

```bash
# Test individual components
python -c "from src.grid_core import optimize_grid; print('Grid optimization:', optimize_grid('test-region'))"

# Test async NAT functions (development mode)
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

### 📂 Original Version Testing

#### 🚀 Full Integration Testing

```bash
# Navigate to original structure
cd Grid_optimization

# Run usage examples
python usage_examples.py

# Run NAT integration tests (if aiqtoolkit is installed)
python tests/test_nat_integration.py

# Test with various configurations
aiq run --config_file configs/workflow.yml --input "Test grid optimization"
aiq run --config_file grid_optimization/src/nat_toolkit/configs/unified-config.yml --input "Test all functions"
```

#### 🏗️ Advanced NAT Testing

```bash
# Test legacy compatibility
aiq run --config_file configs/workflow.yml \
        --input "Use nat_grid_optimization/optimize_grid for testing"

# Test reasoning agent
aiq run --config_file grid_optimization/src/nat_toolkit/configs/config-reasoning.yml \
        --input "Analyze grid performance and provide recommendations"

# Test with NVIDIA NIM models (requires API key)
export NVIDIA_API_KEY="your-key"
aiq run --config_file configs/workflow.yml \
        --input "Optimize grid using NVIDIA models" \
        --llm nim_llm
```

**Test Coverage:**
- ✅ **NAT Integration** - AI agent function testing
- ✅ **API Endpoints** - REST API functionality
- ✅ **Core Grid Logic** - Optimization algorithms
- ✅ **Database Operations** - Data persistence
- ✅ **Security** - Access control and validation

## 🔥 Unified NAT Integration

The system features a **completely integrated NVIDIA NeMo Agent Toolkit** with both modern and legacy support:

### 🔧 Modern Functions (Recommended)
| Function | Purpose | Example |
|----------|---------|---------|
| **`grid_optimize`** | Advanced optimization with analysis | `"Optimize grid for us-west"` |
| **`grid_status`** | Real-time monitoring & alerts | `"Show current grid status"` |
| **`grid_analyze`** | Performance trends & insights | `"Analyze efficiency trends"` |

### 🔄 Legacy Compatibility
| Legacy Function | Modern Equivalent | Status |
|----------------|-------------------|--------|
| `nat_grid_optimization/optimize_grid` | `grid_optimize` | ✅ Supported |
| `nat_grid_optimization/show_last_optimization` | `grid_status` | ✅ Supported |

### 📋 Configuration Options
- **`configs/workflow.yml`** - Unified modern workflow
- **`configs/workflow-reasoning.yml`** - Advanced reasoning
- **`src/nat_toolkit/configs/unified-config.yml`** - Complete feature set
- **Legacy configs** - Automatically compatible

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

### 📊 Monitoring & Observability

| Feature | Endpoint/Method | Description |
|---------|----------------|-------------|
| **Health Checks** | `GET /health` | Service health status |
| **API Documentation** | `GET /docs` | Interactive Swagger UI |
| **Logs** | `logs/` directory | Structured application logs |
| **Metrics** | Built-in monitoring | Performance and usage metrics |

## 📚 Documentation & Resources

| Resource | Location | Description |
|----------|----------|-------------|
| **API Docs** | http://localhost:8000/docs | Interactive OpenAPI documentation |
| **Quick Start** | This README | Installation and basic usage |
| **Configuration** | `configs/` directory | NAT workflow configurations |
| **Deployment** | `deployment/DEPLOYMENT.md` | Production deployment guide |
| **Development** | `Makefile` | Development commands and tools |

## 🤝 Contributing

We welcome contributions! Please follow these steps:

### Development Workflow

```bash
# 1. Fork and clone
git clone https://github.com/your-username/grid-optimization.git
cd grid-optimization

# 2. Set up development environment
make install-dev

# 3. Create feature branch
git checkout -b feature/your-amazing-feature

# 4. Make changes and test
make test
make lint
make format

# 5. Commit and push
git commit -m "Add amazing feature"
git push origin feature/your-amazing-feature

# 6. Open Pull Request
```

### Code Quality Tools

| Tool | Command | Purpose |
|------|---------|---------|
| **Tests** | `make test` | Run full test suite |
| **Linting** | `make lint` | Check code style |
| **Formatting** | `make format` | Auto-format code |
| **Type Check** | `make type-check` | Static type analysis |

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NVIDIA NeMo Agent Toolkit** - Core AI agent framework
- **FastAPI** - High-performance web framework
- **SQLAlchemy** - Database ORM and management
- **OpenAI** - Language model APIs
- **NVIDIA NIM** - High-performance model inference

## 📞 Support & Community

| Resource | Link | Description |
|----------|------|-------------|
| **🐛 Issues** | [GitHub Issues](https://github.com/grid-optimization/issues) | Bug reports and feature requests |
| **💬 Discussions** | [GitHub Discussions](https://github.com/grid-optimization/discussions) | Community Q&A and ideas |
| **📖 Wiki** | [Project Wiki](https://github.com/grid-optimization/wiki) | Additional documentation |
| **🏷️ Releases** | [GitHub Releases](https://github.com/grid-optimization/releases) | Version history and downloads |

## ⭐ Quick Commands Reference

### ✨ Clean Version Commands

```bash
# Setup and Testing (Production Ready)
cd Grid_optimization_clean/grid_optimization
python -m venv .venv && source .venv/bin/activate
pip install -e .
python -c "from src.grid_core.db import init_db; init_db()"
python test_core.py                    # Complete system test

# Component Testing
python -c "from src.grid_core import optimize_grid; print(optimize_grid('test'))"
python -c "from src.grid_core.security import validate_region_access; print(validate_region_access('us-west'))"
```

### 📂 Original Version Commands

```bash
# Setup and Full Integration
cd Grid_optimization
python -m venv .venv && source .venv/bin/activate  
pip install -e ".[dev]"
python usage_examples.py              # Usage demonstration

# NAT Integration (requires aiqtoolkit)
pip install aiqtoolkit
aiq run --config_file configs/workflow.yml --input "Optimize grid for us-west"
aiq run --config_file grid_optimization/src/nat_toolkit/configs/unified-config.yml --input "Show analysis"
```

### 🤖 Advanced NAT Commands

```bash
# Modern functions
aiq run --config_file configs/workflow.yml --input "Use grid_optimize for us-west region"
aiq run --config_file configs/workflow.yml --input "Show grid_status for all regions"

# Legacy compatibility
aiq run --config_file configs/workflow.yml --input "Use nat_grid_optimization/optimize_grid"

# Reasoning agent
aiq run --config_file grid_optimization/src/nat_toolkit/configs/config-reasoning.yml --input "Analyze trends"

# NVIDIA NIM models
export NVIDIA_API_KEY="your-key"
aiq run --config_file configs/workflow.yml --input "Optimize with NVIDIA models" --llm nim_llm
```

### 🐳 Docker Commands

```bash
# Docker deployment (both versions support)
docker-compose -f deployment/docker-compose.yml up --build
docker-compose -f deployment/docker-compose.yml up -d  # Production mode
```

---

<div align="center">

**🔋 Built with ❤️ for intelligent power grid management**

*Powered by NVIDIA NeMo Agent Toolkit • FastAPI • Python 3.11+*

</div>