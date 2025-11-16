#!/usr/bin/env python3
"""
Test using 'cu' command instead of pyserial
Author: David Broggy
"""

import subprocess
import time
import sys

def main():
    port = "/dev/cu.usbmodem214201"

    print(f"Connecting to {port} using 'cu' command...")
    print("Will send commands and capture output")
    print("-" * 60)

    # Commands to send
    commands = [
        "",      # Enter to wake menu
        "g",     # Display Functions
        "g",     # GUI Functions
        "p",     # Show Text Display
        "MVP Summit 2026\nTest Badge"  # The text to display
    ]

    # Build cu command with input
    input_text = "\n".join(commands) + "\n~.\n"  # ~. exits cu

    try:
        result = subprocess.run(
            ["cu", "-l", port, "-s", "115200"],
            input=input_text.encode(),
            capture_output=True,
            timeout=10
        )

        print("Output:")
        print(result.stdout.decode('utf-8', errors='replace'))

        if result.stderr:
            print("\nErrors:")
            print(result.stderr.decode('utf-8', errors='replace'))

        print("-" * 60)
        print("Check badge display!")

    except subprocess.TimeoutExpired:
        print("Timeout - cu command didn't exit properly")
    except FileNotFoundError:
        print("'cu' command not found")
    except Exception as e:
        print(f"Error: {e}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
