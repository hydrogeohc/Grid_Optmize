"""
Basic tests for Grid Optimization system.
Tests core modules that don't require NeMo Agent Toolkit.
"""

import os
import sys
from datetime import datetime

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

# Add the grid_core module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from grid_core.db import Base, GridState, OptimizationResult, create_tables, get_engine, get_session


class TestDatabase:
    """Test database functionality."""

    @pytest.fixture
    def test_engine(self):
        """Create a test database engine."""
        engine = create_engine("sqlite:///:memory:")
        create_tables(engine)
        return engine

    @pytest.fixture
    def test_session(self, test_engine):
        """Create a test database session."""
        Session = sessionmaker(bind=test_engine)
        session = Session()
        yield session
        session.close()

    def test_engine_creation(self):
        """Test database engine creation."""
        engine = get_engine("sqlite:///:memory:")
        assert engine is not None

    def test_table_creation(self, test_engine):
        """Test that tables are created successfully."""
        # Check that tables exist using inspector
        inspector = inspect(test_engine)
        tables = inspector.get_table_names()
        assert "grid_state" in tables
        assert "optimization_result" in tables

    def test_grid_state_model(self, test_session):
        """Test GridState model operations."""
        # Create a grid state record
        grid_state = GridState(region="test-region", demand=100.0, supply=110.0)

        test_session.add(grid_state)
        test_session.commit()

        # Query the record
        retrieved = test_session.query(GridState).filter_by(region="test-region").first()
        assert retrieved is not None
        assert retrieved.region == "test-region"
        assert retrieved.demand == 100.0
        assert retrieved.supply == 110.0
        assert isinstance(retrieved.timestamp, datetime)

    def test_optimization_result_model(self, test_session):
        """Test OptimizationResult model operations."""
        # Create an optimization result record
        opt_result = OptimizationResult(
            region="test-region", optimized_supply=105.0, optimized_demand=95.0, losses=5.0
        )

        test_session.add(opt_result)
        test_session.commit()

        # Query the record
        retrieved = test_session.query(OptimizationResult).filter_by(region="test-region").first()
        assert retrieved is not None
        assert retrieved.region == "test-region"
        assert retrieved.optimized_supply == 105.0
        assert retrieved.optimized_demand == 95.0
        assert retrieved.losses == 5.0
        assert isinstance(retrieved.timestamp, datetime)


class TestGridOperations:
    """Test core grid operations that don't require AI agents."""

    def test_import_operations(self):
        """Test that we can import core operations module."""
        from grid_core import operations

        assert operations is not None
        # Test that the functions are available
        assert hasattr(operations, "optimize_grid")
        assert hasattr(operations, "get_latest_optimization")

    def test_import_tools(self):
        """Test that we can import grid tools."""
        from grid_core.tools import grid_tools

        assert grid_tools is not None
        # Test that the functions are available
        assert hasattr(grid_tools, "optimize_grid")
        assert hasattr(grid_tools, "show_last_optimization")

    def test_optimize_grid_function(self):
        """Test the optimize_grid function with test data."""
        from grid_core.db import create_tables, get_engine, get_session
        from grid_core.tools.grid_tools import optimize_grid

        # Create in-memory test database
        engine = create_engine("sqlite:///:memory:")
        create_tables(engine)
        session = get_session(engine)

        # Add test data
        grid_state = GridState(region="test-region", demand=100.0, supply=110.0)
        session.add(grid_state)
        session.commit()
        session.close()

        # Test optimization (it will use the default database, but that's ok for testing)
        result = optimize_grid("nonexistent-region")

        # Should return error for non-existent region
        assert "error" in result


class TestConfiguration:
    """Test configuration and setup."""

    def test_workflow_config_exists(self):
        """Test that workflow configuration file exists."""
        config_path = os.path.join(os.path.dirname(__file__), "test", "workflow.yml")
        assert os.path.exists(config_path), "Workflow configuration not found"

    def test_requirements_file_exists(self):
        """Test that requirements.txt exists."""
        req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
        assert os.path.exists(req_path), "requirements.txt not found"

    def test_setup_file_exists(self):
        """Test that setup.py exists."""
        setup_path = os.path.join(os.path.dirname(__file__), "setup.py")
        assert os.path.exists(setup_path), "setup.py not found"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
