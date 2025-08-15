"""
Initialize test data for the Grid Optimization system.
This creates sample grid state data for testing purposes.
"""

from datetime import UTC, datetime, timedelta

from .database import GridState, create_tables, get_engine, get_session


def init_test_data():
    """Initialize the database with sample grid state data."""
    engine = get_engine()
    create_tables(engine)
    session = get_session(engine)

    # Clear existing data
    session.query(GridState).delete()
    session.commit()

    # Create sample data for different regions
    test_data = [
        {"region": "us-west", "demand": 1000.0, "supply": 1100.0},
        {"region": "us-east", "demand": 1500.0, "supply": 1550.0},
        {"region": "us-central", "demand": 800.0, "supply": 850.0},
        {"region": "pgae", "demand": 1200.0, "supply": 1250.0},
    ]

    # Add data with timestamps spread over the last few days
    base_time = datetime.now(UTC) - timedelta(days=2)

    for i, data in enumerate(test_data):
        # Add multiple entries for each region to simulate time series data
        for j in range(3):
            timestamp = base_time + timedelta(hours=i * 6 + j * 2)
            # Add some variation to the values
            demand_var = data["demand"] + (j * 10 - 10)  # -10, 0, +10
            supply_var = data["supply"] + (j * 15 - 15)  # -15, 0, +15

            grid_state = GridState(
                region=data["region"], demand=demand_var, supply=supply_var, timestamp=timestamp
            )
            session.add(grid_state)

    session.commit()
    session.close()

    print(f"Added {len(test_data) * 3} test grid state records")


if __name__ == "__main__":
    init_test_data()
    print("Test data initialization completed!")
