#!/usr/bin/env python3
"""
Badge Display Test using pexpect
Author: David Broggy
"""

import sys
import pexpect
import time

def main():
    # Use Display Processor port
    port = "/dev/cu.usbmodem214201"

    print(f"Connecting to Display Processor: {port}...")
    print("=" * 60)

    try:
        # Open serial connection using picocom command
        # Use longer timeout since badge needs time to boot and respond
        child = pexpect.spawn(f'picocom -b 115200 {port}', encoding='utf-8', timeout=10)
        child.logfile = sys.stdout  # Show all output

        print("\n[1/5] Connected! Waiting for Terminal ready...")
        # Wait for picocom to be ready
        child.expect('Terminal ready', timeout=10)
        print("✓ Terminal ready")

        print("\n[2/5] Sending Enter to wake menu...")
        child.sendline('')
        time.sleep(1)
        child.sendline('')  # Send twice to be sure
        child.expect('Enter Letter:', timeout=10)
        print("✓ Main menu displayed")

        print("\n[3/6] Navigating to Display Functions (press 'g')...")
        child.sendline('g')
        child.expect('Display Functions', timeout=10)
        child.expect('Enter Letter:', timeout=10)
        print("✓ In Display Functions menu")

        print("\n[4/6] Navigating to GUI Functions (press 'g')...")
        child.sendline('g')
        child.expect('GUI Functions', timeout=10)
        child.expect('Enter Letter:', timeout=10)
        print("✓ In GUI Functions menu")

        print("\n[5/6] Selecting Show Text Display (press 'p')...")
        child.sendline('p')
        child.expect('Enter Text To Display', timeout=10)
        print("✓ Ready to enter text")

        print("\n[6/6] Sending text: 'MVP Summit 2026'...")
        child.sendline('MVP Summit 2026')
        time.sleep(3)  # Wait for display to update

        print("\n" + "=" * 60)
        print("✓ TEXT SENT!")
        print("CHECK YOUR BADGE DISPLAY NOW!")
        print("=" * 60)

        # Exit picocom (send Ctrl+A Ctrl+X)
        child.sendcontrol('a')
        child.sendcontrol('x')
        child.close()

        return 0

    except pexpect.TIMEOUT as e:
        print(f"\n✗ Timeout: {e}")
        print("Last output:")
        print(child.before)
        return 1
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
