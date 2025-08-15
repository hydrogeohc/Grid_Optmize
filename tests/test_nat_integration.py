"""
Test NAT (NeMo Agent Toolkit) Integration
Tests the grid optimization NAT toolkit functions
"""

import asyncio
import os
import sys

import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

try:
    from grid_core.nat_integration import (
        analyze_grid_metrics,
        get_optimization_status,
        optimize_grid_region,
    )
except ImportError:
    # Fallback functions for testing
    async def optimize_grid_region(region):
        return {"status": "success", "region": region, "timestamp": "test"}

    async def get_optimization_status(region):
        return {"region": region, "current_status": "test"}

    async def analyze_grid_metrics(region, metric):
        return {"region": region, "metric": metric}


class TestNATIntegration:
    """Test NAT integration functions."""

    @pytest.mark.asyncio
    async def test_optimize_grid_region(self):
        """Test async grid optimization function."""
        result = await optimize_grid_region("test-region")

        assert isinstance(result, dict)
        assert "status" in result
        assert "region" in result
        assert "timestamp" in result
        assert result["region"] == "test-region"

        # Should either succeed or fail gracefully
        if result["status"] == "success":
            assert "optimization_time" in result
            assert "loss_reduction" in result
        else:
            assert "message" in result

    @pytest.mark.asyncio
    async def test_get_optimization_status(self):
        """Test grid status retrieval."""
        result = await get_optimization_status("test-region")

        assert isinstance(result, dict)
        assert "region" in result
        assert result["region"] == "test-region"

        if result.get("status") != "error":
            assert "current_status" in result
            assert "active_alerts" in result

    @pytest.mark.asyncio
    async def test_analyze_grid_metrics(self):
        """Test grid metrics analysis."""
        result = await analyze_grid_metrics("test-region", "efficiency")

        assert isinstance(result, dict)
        assert "region" in result
        assert "metric" in result
        assert result["region"] == "test-region"
        assert result["metric"] == "efficiency"

    @pytest.mark.asyncio
    async def test_analyze_load_metrics(self):
        """Test load-specific analysis."""
        result = await analyze_grid_metrics("test-region", "load")

        assert isinstance(result, dict)
        assert result["metric"] == "load"

    def test_sync_to_async_compatibility(self):
        """Test that functions can be called in async context."""

        async def run_test():
            tasks = [
                optimize_grid_region("region-1"),
                get_optimization_status("region-2"),
                analyze_grid_metrics("region-3", "efficiency"),
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # All should return results, not raise exceptions
            for result in results:
                assert not isinstance(result, Exception)
                assert isinstance(result, dict)

        # Run the async test
        asyncio.run(run_test())

    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling for invalid inputs."""
        # Test with invalid region
        result = await optimize_grid_region("")
        assert result["status"] == "error"

        # Test with None region
        result = await get_optimization_status(None)
        assert isinstance(result, dict)  # Should handle gracefully

    def test_function_signatures(self):
        """Test that functions have correct signatures for NAT compatibility."""
        import inspect

        # Check optimize_grid_region signature
        sig = inspect.signature(optimize_grid_region)
        assert len(sig.parameters) == 1
        assert "region" in sig.parameters
        assert sig.parameters["region"].default == "default"

        # Check get_optimization_status signature
        sig = inspect.signature(get_optimization_status)
        assert len(sig.parameters) == 1
        assert "region" in sig.parameters

        # Check analyze_grid_metrics signature
        sig = inspect.signature(analyze_grid_metrics)
        assert len(sig.parameters) == 2
        assert "region" in sig.parameters
        assert "metric" in sig.parameters


if __name__ == "__main__":
    # Simple test runner for development
    async def run_basic_tests():
        print("Testing NAT Integration...")

        print("1. Testing grid optimization...")
        result = await optimize_grid_region("test")
        print(f"   Result: {result.get('status', 'unknown')}")

        print("2. Testing status retrieval...")
        result = await get_optimization_status("test")
        print(f"   Found region data: {'current_status' in result}")

        print("3. Testing metrics analysis...")
        result = await analyze_grid_metrics("test", "efficiency")
        print(f"   Analysis completed: {'metric' in result}")

        print("NAT Integration tests completed!")

    # Run basic tests if script is executed directly
    asyncio.run(run_basic_tests())
