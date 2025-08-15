#!/usr/bin/env python3
"""
Grid Optimization Test Runner

This script runs the complete test suite for the Grid Optimization project.
It includes both unit tests and API tests.
"""

import os
import subprocess
import sys


def run_tests():
    """Run the complete test suite and return results."""

    print("🔬 Grid Optimization Test Suite")
    print("=" * 50)

    # Test files to run
    test_files = ["test_basic.py", "test_api.py"]

    # Check if test files exist
    missing_files = []
    for test_file in test_files:
        if not os.path.exists(test_file):
            missing_files.append(test_file)

    if missing_files:
        print(f"❌ Missing test files: {missing_files}")
        return False

    # Run tests with pytest
    cmd = [sys.executable, "-m", "pytest", "-v", "--tb=short", "--color=yes"] + test_files

    print("Running tests...")
    print(" ".join(cmd))
    print()

    result = subprocess.run(cmd, capture_output=False)

    if result.returncode == 0:
        print("\n✅ All tests passed!")
        return True
    else:
        print(f"\n❌ Tests failed with return code {result.returncode}")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
