#!/usr/bin/env python3
"""
Basic Badge Connectivity Test
Author: David Broggy

Simple test to verify badge is connected and can display text.
"""

import sys
import time

def main():
    print("=" * 50)
    print("BASIC BADGE TEST")
    print("=" * 50)

    # Step 1: Import freewili
    print("\n[1/3] Importing freewili library...")
    try:
        from freewili.fw import FreeWili
        print("✓ freewili imported successfully")
    except ImportError as e:
        print("✗ ERROR: freewili not installed")
        print("\nInstall with: pip install freewili")
        return 1

    # Step 2: Find badge
    print("\n[2/3] Searching for badge...")
    try:
        result = FreeWili.find_first()
        if result.is_err():
            print("✗ ERROR: No badges found")
            print(f"  {result.unwrap_err()}")
            print("\nTroubleshooting:")
            print("  - Is the badge plugged in via USB?")
            print("  - Does it show up in 'ls /dev/cu.usbmodem*'?")
            print("  - Is FREE-WILi firmware installed?")
            return 1

        badge = result.unwrap()
        print("✓ Found badge")
        print(f"  Connected to badge")
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return 1

    # Step 3: Display test message
    print("\n[3/3] Displaying test message...")
    try:
        result = badge.show_text_display("Hello World!\n\nBasic Test\nWorking!")

        if result.is_ok():
            print("✓ Text displayed successfully!")
            print("\nCHECK YOUR BADGE - You should see:")
            print("  'Hello World!'")
            print("  'Basic Test'")
            print("  'Working!'")
            print("\n" + "=" * 50)
            print("SUCCESS - Badge is working!")
            print("=" * 50)
            return 0
        else:
            print(f"✗ ERROR: {result.unwrap_err()}")
            return 1

    except Exception as e:
        print(f"✗ ERROR: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
