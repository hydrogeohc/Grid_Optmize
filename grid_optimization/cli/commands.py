#!/usr/bin/env python3
"""
Grid Optimization CLI Commands

Consolidated command line interface for all grid optimization operations.
"""

import argparse
import sys
from pathlib import Path
from typing import List

from core.operations import get_latest_optimization, optimize_grid

# Add package to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def run_optimization(regions: List[str]) -> None:
    """Run grid optimization for specified regions."""
    print("🔌 Grid Optimization System")
    print("=" * 50)

    available_regions = ["us-west", "us-east", "us-central", "pgae"]

    for region in regions:
        if region not in available_regions:
            print(f"❌ Unknown region '{region}'. Skipping.")
            continue

        print(f"\n🌍 Optimizing grid for region: {region.upper()}")
        print("-" * 30)

        try:
            result = optimize_grid(region)

            if "error" in result:
                print(f"❌ Error: {result['error']}")
                continue

            # Display results
            print("✅ Optimization Complete!")
            print(f"📊 Region: {result['region'].upper()}")
            print(f"⚡ Optimized Supply: {result['optimized_supply']:.2f} MW")
            print(f"📈 Optimized Demand: {result['optimized_demand']:.2f} MW")
            print(f"💸 Power Losses: {result['losses']:.8f} MW²")
            print(f"📊 Grid Efficiency: {result['efficiency']:.6f}%")
            print(f"💰 Annual Savings: ${result['cost_savings']:,}")

        except Exception as e:
            print(f"❌ Optimization failed for {region}: {e}")


def show_last_optimization(region: str) -> None:
    """Show the last optimization results for a region."""
    try:
        result = get_latest_optimization(region)

        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return

        print(f"🔍 Latest Optimization History for {region.upper()}:")
        print("-" * 50)
        print(f"🕒 Timestamp: {result.get('timestamp', 'N/A')}")
        print(f"⚡ Supply: {result.get('optimized_supply', 'N/A'):.2f} MW")
        print(f"📈 Demand: {result.get('optimized_demand', 'N/A'):.2f} MW")
        print(f"💸 Losses: {result.get('losses', 'N/A'):.8f} MW²")

    except Exception as e:
        print(f"❌ Failed to retrieve optimization data: {e}")


def test_all_regions() -> None:
    """Test optimization on all available regions."""
    regions = ["us-west", "us-east", "us-central", "pgae"]

    print("🧪 Testing All Regions")
    print("=" * 50)

    success_count = 0

    for region in regions:
        print(f"\n🔬 Testing {region}...")
        try:
            result = optimize_grid(region)
            if "error" not in result:
                print(f"✅ {region}: Success")
                success_count += 1
            else:
                print(f"❌ {region}: {result['error']}")
        except Exception as e:
            print(f"❌ {region}: {e}")

    print(f"\n📊 Test Results: {success_count}/{len(regions)} regions successful")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Grid Optimization CLI - Comprehensive grid management tool"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Optimize command
    optimize_parser = subparsers.add_parser("optimize", help="Optimize grid for regions")
    optimize_parser.add_argument(
        "regions", nargs="*", default=["us-west"], help="Regions to optimize (default: us-west)"
    )

    # Status command
    status_parser = subparsers.add_parser("status", help="Show last optimization")
    status_parser.add_argument(
        "region", default="us-west", nargs="?", help="Region to check status for (default: us-west)"
    )

    # Test command
    subparsers.add_parser("test", help="Test all regions")

    # Interactive mode
    subparsers.add_parser("interactive", help="Interactive mode")

    args = parser.parse_args()

    if not args.command:
        # Default interactive mode if no command specified
        args.command = "interactive"

    if args.command == "optimize":
        run_optimization(args.regions)
    elif args.command == "status":
        show_last_optimization(args.region)
    elif args.command == "test":
        test_all_regions()
    elif args.command == "interactive":
        # Interactive mode - original script behavior
        available_regions = ["us-west", "us-east", "us-central", "pgae"]
        print(f"📍 Available regions: {', '.join(available_regions)}")
        print()

        region = input("Enter region to optimize (or press Enter for us-west): ").strip()
        if not region:
            region = "us-west"

        run_optimization([region])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
