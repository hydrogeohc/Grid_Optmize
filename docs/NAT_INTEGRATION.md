# NAT Toolkit Integration Guide

Complete guide to the NVIDIA NeMo Agent Toolkit (NAT) integration in the Grid Optimization System.

## Overview

The Grid Optimization System provides seamless integration with NVIDIA's NeMo Agent Toolkit (NAT), enabling AI-powered grid operations through conversational interfaces and autonomous agents.

## Features

### ✅ What's Working
- **Entry Point Discovery**: Functions automatically discoverable by AIQ
- **Async Operations**: Non-blocking grid optimizations
- **Multi-Region Support**: All regions (us-west, us-east, us-central, pgae)
- **Error Handling**: Robust error management and validation
- **Performance**: Sub-second optimization times
- **Function Registration**: Properly registered with AIQ components

### ⚠️ Known Limitations
- **LLM Framework Compatibility**: OpenAI/LangChain integration needs resolution on macOS
- **AIQ Version**: Some features require specific AIQ toolkit versions

## Available NAT Functions

### 1. `optimize_grid_region(region: str)`
**Optimize power grid for a specific region**

```python
import asyncio
from grid_optimization.integrations.nat.register import optimize_grid_region

async def optimize():
    result = await optimize_grid_region('us-west')
    print(f"Status: {result['status']}")
    print(f"Supply: {result['optimized_supply']:.2f} MW")
    print(f"Demand: {result['optimized_demand']:.2f} MW")
    print(f"Losses: {result['losses']:.2e} MW²")

asyncio.run(optimize())
```

### 2. `get_optimization_status(region: str)`
**Get optimization status and history for a region**

```python
async def check_status():
    status = await get_optimization_status('us-west')
    print(f"Status: {status['status']}")
    if status['status'] == 'success':
        print(f"Region: {status['region']}")
        print(f"Last optimized: {status.get('timestamp', 'Unknown')}")

asyncio.run(check_status())
```

### 3. `analyze_grid_metrics(region: str)`
**Analyze grid performance metrics**

```python
async def analyze():
    metrics = await analyze_grid_metrics('us-west')
    print(f"Analysis: {metrics}")

asyncio.run(analyze())
```

## AIQ Integration

### Entry Points Configuration

The system registers NAT functions as AIQ components via entry points:

```toml
# pyproject.toml
[project.entry-points."aiq.components"]
"nat_toolkit/optimize_grid" = "grid_optimization.integrations.nat.register:LegacyOptimizeGridConfig"
"nat_toolkit/show_last_optimization" = "grid_optimization.integrations.nat.register:LegacyShowOptimizationConfig"
```

### AIQ Configuration

#### Basic Configuration (`configs/aiq/basic.yml`)
```yaml
general:
  use_uvloop: true

llms:
  grid_llm:
    _type: openai
    model_name: gpt-4o-mini
    temperature: 0.1
    max_tokens: 1024

functions:
  current_datetime:
    _type: current_datetime
  optimize_grid:
    _type: optimize_grid
  show_last_optimization:
    _type: show_last_optimization

workflow:
  _type: react_agent
  tool_names:
    - optimize_grid
    - show_last_optimization
    - current_datetime
  llm_name: grid_llm
  verbose: true
  system_message: |
    You are a grid optimization assistant. You can optimize power grids 
    for different regions and show optimization results.
    
    Available regions: us-west, us-east, us-central, pgae
```

#### Full Configuration (`configs/aiq/full.yml`)
```yaml
# Enhanced configuration with multiple LLMs and advanced features
general:
  use_uvloop: true

llms:
  grid_llm:
    _type: openai
    model_name: gpt-4o
    max_tokens: 4096
    temperature: 0.1
    
  backup_llm:
    _type: openai
    model_name: gpt-4o-mini
    max_tokens: 2048
    temperature: 0.1

functions:
  current_datetime:
    _type: current_datetime
  optimize_grid:
    _type: optimize_grid
  show_last_optimization:
    _type: show_last_optimization

workflow:
  _type: react_agent
  tool_names:
    - optimize_grid
    - show_last_optimization
    - current_datetime
  llm_name: grid_llm
  verbose: true
  system_message: |
    You are an advanced grid optimization assistant with comprehensive 
    capabilities for power grid management and analysis.
```

### Usage with AIQ

#### Prerequisites
```bash
# Install required packages
uv pip install -e .

# Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
```

#### Running with AIQ
```bash
# Basic usage
aiq run --config_file configs/aiq/basic.yml --input "Optimize grid for us-west"

# Advanced usage with full config
aiq run --config_file configs/aiq/full.yml --input "Analyze grid performance for us-east and provide recommendations"
```

#### Example Interactions
```
User: "Optimize the grid for us-west region"
Assistant: I'll optimize the grid for the us-west region...
[Calls optimize_grid function]
Result: Grid optimized successfully! Supply: 1010.00 MW, Demand: 1010.00 MW, Losses: 4.57e-12 MW²

User: "Show me the last optimization for us-east"
Assistant: Let me retrieve the latest optimization data for us-east...
[Calls show_last_optimization function]
Result: Last optimization for us-east: Supply: 1510.00 MW, completed at 10:30 AM
```

## Testing NAT Integration

### Comprehensive Test Suite

Run the complete NAT testing suite:
```bash
python scripts/comprehensive_nat_test.py
```

### Test Results
- **Core Functions**: 4/4 regions passed
- **NAT Async Functions**: 4/4 regions passed
- **NAT Status Functions**: 4/4 regions passed
- **Performance**: All regions < 0.01s average
- **AIQ Integration**: 2/2 entry points loaded successfully
- **Overall Success Rate**: 93.8%

### Manual Testing
```python
# Test individual functions
import asyncio
from grid_optimization.integrations.nat.register import *

async def test_all():
    # Test optimization
    result = await optimize_grid_region('us-west')
    print(f"Optimization: {result['status']}")
    
    # Test status
    status = await get_optimization_status('us-west')
    print(f"Status: {status['status']}")
    
    # Test metrics
    metrics = await analyze_grid_metrics('us-west')
    print(f"Metrics: {metrics}")

asyncio.run(test_all())
```

## Troubleshooting

### Common Issues

#### 1. Entry Points Not Found
```bash
# Check entry points registration
python -c "from importlib.metadata import entry_points; eps = entry_points().select(group='aiq.components'); [print(ep.name, ep.value) for ep in eps if 'nat_toolkit' in ep.name]"

# Reinstall package if needed
uv pip uninstall grid-optimization && uv pip install -e .
```

#### 2. Function Import Errors
```bash
# Test direct imports
python -c "from grid_optimization.integrations.nat.register import optimize_grid_region; print('Success')"
```

#### 3. AIQ LLM Issues
```bash
# Check OpenAI API key
echo $OPENAI_API_KEY

# Test without LLM (direct functions)
python -c "
import asyncio
from grid_optimization.integrations.nat.register import optimize_grid_region
print(asyncio.run(optimize_grid_region('us-west')))
"
```

### Debug Mode

Enable verbose logging for debugging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your NAT function calls here
```

## Performance Optimization

### Best Practices
1. **Async Usage**: Always use async/await for NAT functions
2. **Connection Pooling**: Reuse database connections
3. **Caching**: Cache optimization results when appropriate
4. **Batching**: Process multiple regions in parallel

### Example Parallel Processing
```python
import asyncio
from grid_optimization.integrations.nat.register import optimize_grid_region

async def optimize_all_regions():
    regions = ['us-west', 'us-east', 'us-central', 'pgae']
    
    # Parallel optimization
    tasks = [optimize_grid_region(region) for region in regions]
    results = await asyncio.gather(*tasks)
    
    for region, result in zip(regions, results):
        print(f"{region}: {result['optimized_supply']:.1f} MW")

asyncio.run(optimize_all_regions())
```

## Integration with Other Systems

### Custom Agents
```python
# Example custom agent integration
class GridOptimizationAgent:
    def __init__(self):
        from grid_optimization.integrations.nat.register import optimize_grid_region
        self.optimize = optimize_grid_region
    
    async def handle_request(self, region: str, parameters: dict):
        result = await self.optimize(region)
        return self.format_response(result)
    
    def format_response(self, result):
        return {
            "status": result["status"],
            "summary": f"Optimized {result['region']} grid: {result['optimized_supply']:.1f} MW supply",
            "efficiency": f"{((result['optimized_supply'] - result['losses']) / result['optimized_supply'] * 100):.2f}%"
        }
```

### Webhook Integration
```python
# Example webhook for notifications
async def optimization_webhook(region: str):
    result = await optimize_grid_region(region)
    
    if result['status'] == 'success':
        # Send notification
        webhook_data = {
            "event": "optimization_complete",
            "region": region,
            "supply": result['optimized_supply'],
            "timestamp": result.get('timestamp')
        }
        # Post to webhook URL
```

## Future Enhancements

### Planned Features
- **Streaming Results**: Real-time optimization progress
- **Advanced Analytics**: ML-powered grid predictions
- **Multi-Model Support**: Different LLM providers
- **Custom Tools**: User-defined optimization parameters
- **Integration APIs**: REST endpoints for NAT functions

### Contributing
1. Add new NAT functions to `register.py`
2. Update entry points in `pyproject.toml`
3. Add comprehensive tests
4. Update documentation
5. Ensure >90% test success rate

## Support

For NAT integration support:
1. Check function registration with entry points
2. Verify async function signatures
3. Test direct function calls before AIQ integration
4. Review test results for performance baselines
5. Check AIQ logs for detailed error information