# NAT Grid Toolkit

**NVIDIA NeMo Agent Toolkit Integration for Grid Optimization**

## Overview

This module provides NAT (NVIDIA NeMo Agent Toolkit) integration for the Grid Optimization System. The core grid optimization functions work independently, while NAT provides AI agent capabilities when configured with an OpenAI API key.

## Quick Start

### ✅ Working Grid Optimization (No Setup Required)

```bash
# Test all regions
python scripts/test_all_regions.py

# Interactive optimization  
echo "us-west" | python scripts/run_grid_optimization.py

# Direct Python API
python -c "
import sys; sys.path.insert(0, 'src')
from grid_optimization.core.operations import optimize_grid
print(optimize_grid('us-west'))
"
```

### ⚠️ NAT Integration (Requires OpenAI API Key)

```bash
# 1. Set API key
export OPENAI_API_KEY="your-key"

# 2. Use NAT commands
aiq run --config_file configs/workflow.yml \
        --input "Optimize the grid for region us-west"
```

## Available Functions

### Core Functions (Always Available)
- `optimize_grid(region)` - Direct grid optimization
- `get_latest_optimization(region)` - Get optimization history

### NAT Functions (Requires OpenAI API Key)
- `nat_toolkit/optimize_grid` - NAT-wrapped optimization
- `nat_toolkit/show_last_optimization` - NAT-wrapped status

## Supported Regions
us-west, us-east, us-central

## Troubleshooting

**NAT commands not working?** Use the direct Python scripts:
```bash
python scripts/test_all_regions.py
echo "us-west" | python scripts/run_grid_optimization.py
```

**Missing OpenAI API key?** Set it or use direct Python API:
```bash
export OPENAI_API_KEY="your-key"  # For NAT features
# OR
python -c "import sys; sys.path.insert(0, '.'); from grid_optimization.core.operations import optimize_grid; print(optimize_grid('us-west'))"
```

## Technical Details

This module registers NAT functions via entry points in `pyproject.toml` and provides async wrappers around the core grid optimization functions in `../core/operations.py`. The NAT integration requires an OpenAI API key for LLM functionality, while the core optimization algorithms work independently.