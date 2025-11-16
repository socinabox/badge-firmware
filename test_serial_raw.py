#!/usr/bin/env python3
"""
Raw Serial Test - Just listen for any data
Author: David Broggy
"""

import sys
import time
import serial
import serial.tools.list_ports

def main():
    # Find port
    ports = [p.device for p in serial.tools.list_ports.comports() if 'usbmodem' in p.device]
    if not ports:
        print("No badge found")
        return 1

    port = ports[0]
    print(f"Opening {port}...")

    # Open serial
    ser = serial.Serial(port, 115200, timeout=0.1)
    print("Port opened.")

    # Wait a moment for initial banner
    time.sleep(1)

    # Read any initial data
    print("Reading initial output...")
    print("-" * 60)
    if ser.in_waiting:
        data = ser.read(ser.in_waiting)
        print(data.decode('utf-8', errors='replace'))

    print("\nListening for 10 seconds...")
    print("Press buttons on the badge or it might output menu data")
    print("-" * 60)

    start = time.time()
    while time.time() - start < 10:
        # Send newline every 2 seconds
        if int(time.time() - start) % 2 == 0:
            ser.write(b"\n")
            print("\n[Sent newline]", flush=True)
            time.sleep(0.1)

        # Read any data
        if ser.in_waiting:
            data = ser.read(ser.in_waiting)
            try:
                print(data.decode('utf-8', errors='replace'), end='', flush=True)
            except:
                print(f"[Binary: {data.hex()}]", flush=True)

        time.sleep(0.1)

    print("\n" + "-" * 60)
    print("Done. Did you see any output?")
    ser.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
