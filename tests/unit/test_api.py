"""
API tests for Grid Optimization FastAPI server.
Tests the real server implementation with the fallback runtime.
"""

import os
import sys

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add current directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from grid_core.db import Base, GridState, create_tables
from grid_core.init_test_data import init_test_data


@pytest.fixture(scope="session")
def setup_test_db():
    """Set up a test database with sample data."""
    # Initialize test database and data
    init_test_data()
    yield
    # Cleanup could go here if needed


class TestGridOptimizationAPI:
    """Test the Grid Optimization API endpoints."""

    def test_import_server(self):
        """Test that we can import the server with fallback runtime."""
        import server

        assert server.app is not None
        assert server.AIQ_AVAILABLE is False  # Should be using fallback

    def test_health_endpoint(self, setup_test_db):
        """Test health endpoint."""
        import test_server

        client = TestClient(test_server.app)
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "runtime_initialized" in data
        assert "version" in data

    def test_metrics_endpoint(self, setup_test_db):
        """Test metrics endpoint."""
        import test_server

        client = TestClient(test_server.app)
        response = client.get("/metrics")

        assert response.status_code == 200
        data = response.json()
        # Should have runtime info since test server initializes it
        assert "runtime_status" in data
        assert data["runtime_status"] == "active"

    def test_ask_endpoint_optimize(self, setup_test_db):
        """Test ask endpoint with optimization request."""
        import test_server

        client = TestClient(test_server.app)
        response = client.post("/ask", json={"input": "Optimize the grid", "region": "us-west"})

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "metadata" in data
        assert data["metadata"]["region"] == "us-west"

    def test_ask_endpoint_show_results(self, setup_test_db):
        """Test ask endpoint with show results request."""
        import test_server

        # First optimize to create some results
        client = TestClient(test_server.app)
        client.post("/ask", json={"input": "Optimize the grid", "region": "us-west"})

        # Now ask for results
        response = client.post(
            "/ask", json={"input": "Show last optimization results", "region": "us-west"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_optimize_region_endpoint(self, setup_test_db):
        """Test the region optimization endpoint."""
        import test_server

        client = TestClient(test_server.app)
        response = client.post("/optimize/us-east")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["region"] == "us-east"
        assert "optimization_result" in data

    def test_status_endpoint(self, setup_test_db):
        """Test the status endpoint for a region."""
        import test_server

        # First optimize to create results
        client = TestClient(test_server.app)
        client.post("/optimize/us-central")

        # Now check status
        response = client.get("/status/us-central")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["region"] == "us-central"
        assert "status" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
