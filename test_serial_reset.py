#!/usr/bin/env python3
"""
Serial Test with Hardware Reset
Author: David Broggy
"""

import sys
import time
import serial
import serial.tools.list_ports

def main():
    # Find port - try tty version first (macOS)
    ports = [p.device for p in serial.tools.list_ports.comports() if 'usbmodem' in p.device]
    if not ports:
        print("No badge found")
        return 1

    # Prefer /dev/tty.* over /dev/cu.* on macOS
    port = ports[0]
    if port.startswith('/dev/cu.'):
        tty_port = port.replace('/dev/cu.', '/dev/tty.')
        try:
            # Check if tty version exists
            import os
            if os.path.exists(tty_port):
                port = tty_port
                print(f"Using tty device instead of cu device")
        except:
            pass

    print(f"Opening {port}...")

    # Open with DTR/RTS low to trigger reset
    ser = serial.Serial(
        port=port,
        baudrate=115200,
        timeout=0.1,
        rtscts=False,
        dsrdtr=False
    )

    print("Triggering hardware reset...")
    # Toggle DTR to reset the badge
    ser.setDTR(False)
    ser.setRTS(False)
    time.sleep(0.1)
    ser.setDTR(True)
    ser.setRTS(True)
    time.sleep(0.1)
    ser.setDTR(False)
    time.sleep(0.5)

    print("Waiting for boot banner...")
    print("-" * 60)

    # Read boot output
    start = time.time()
    while time.time() - start < 5:
        if ser.in_waiting:
            data = ser.read(ser.in_waiting)
            print(data.decode('utf-8', errors='replace'), end='', flush=True)
        time.sleep(0.05)

    print("\n" + "-" * 60)
    print("\nNow sending Enter to get menu...")

    # Send Enter to get menu
    ser.write(b"\n")
    time.sleep(1)

    if ser.in_waiting:
        data = ser.read(ser.in_waiting)
        print(data.decode('utf-8', errors='replace'))
    else:
        print("No response to Enter key")

    ser.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
