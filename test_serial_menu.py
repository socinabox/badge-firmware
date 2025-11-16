#!/usr/bin/env python3
"""
Direct Serial Menu Test
Author: David Broggy

Tests badge display by sending menu commands directly via serial.
Uses the interactive menu system discovered in the terminal session.
"""

import sys
import time
import serial
import serial.tools.list_ports

def find_badge_port():
    """Find the badge USB serial port"""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'usbmodem' in port.device:
            return port.device
    return None

def send_command(ser, command, wait=2.0, expect=None):
    """Send a command and wait for response"""
    print(f"\nSending: {repr(command)}")
    ser.write(command.encode())

    # Wait and collect response
    time.sleep(0.2)  # Initial wait for data to arrive
    response = b""
    timeout = time.time() + wait

    while time.time() < timeout:
        if ser.in_waiting:
            chunk = ser.read(ser.in_waiting)
            response += chunk
            print(chunk.decode('utf-8', errors='ignore'), end='', flush=True)

            # If we got expected response, we can continue
            if expect and expect in response.decode('utf-8', errors='ignore'):
                print(f"\n✓ Got expected response: {repr(expect)}")
                break
        time.sleep(0.1)

    print()  # Newline after response
    return response

def main():
    print("=" * 60)
    print("DIRECT SERIAL MENU TEST")
    print("=" * 60)

    # Find badge
    print("\n[1/4] Finding badge...")
    port = find_badge_port()
    if not port:
        print("✗ No badge found on USB")
        return 1

    print(f"✓ Found badge on {port}")

    # Open serial connection
    print("\n[2/4] Opening serial connection...")
    try:
        ser = serial.Serial(
            port=port,
            baudrate=115200,
            timeout=2,
            write_timeout=2,
            rtscts=False,
            dsrdtr=False
        )
        print("✓ Serial port opened")

        # Try to wake up the badge
        ser.setDTR(False)
        ser.setRTS(False)
        time.sleep(0.5)
        ser.setDTR(True)
        ser.setRTS(True)
        time.sleep(0.5)

        # Clear any existing data
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        print("✓ Badge initialized")

    except Exception as e:
        print(f"✗ ERROR: {e}")
        return 1

    time.sleep(1)  # Let connection stabilize

    # Send several newlines to wake up menu
    print("\nWaking up badge...")
    for i in range(3):
        ser.write(b"\n")
        time.sleep(0.3)

    # Navigate to Display Functions -> GUI Functions -> Show Text Display
    print("\n[3/4] Navigating menu...")

    # Press Enter to wake up menu and wait for main menu
    send_command(ser, "\n", wait=2, expect="Enter Letter:")

    # Press 'g' for Display Functions
    send_command(ser, "g", wait=2, expect="Display Functions")

    # Press 'g' again for GUI Functions
    send_command(ser, "g", wait=2, expect="GUI Functions")

    # Press 'p' for Show Text Display
    send_command(ser, "p", wait=2, expect="Enter Text To Display")

    # Send test text
    print("\n[4/4] Sending test text...")
    test_text = "MVP Summit 2026\nSecurity Badge Test"
    send_command(ser, test_text + "\n", wait=2)

    print("\n" + "=" * 60)
    print("CHECK YOUR BADGE DISPLAY!")
    print("Should show: MVP Summit 2026 / Security Badge Test")
    print("=" * 60)

    ser.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
