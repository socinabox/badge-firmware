# ICS Village Badge Architecture - Findings

Author: David Broggy

## Critical Discovery: Dual-Processor Architecture

The ICS Village badge uses a **dual-processor architecture** that differs significantly from standard embedded development:

### Hardware Architecture

1. **Main Processor: Raspberry Pi RP2350A**
   - Handles logic, GPIO, sensors
   - Entry via: RED button + USB connection
   - Firmware format: UF2 files
   - Our Arduino C++ code uploaded here successfully

2. **Display Processor: Separate RP2040**
   - Controls the 320×240 pixel display
   - Entry via: BLUE button + USB connection
   - Communicates with Main Processor via USB serial protocol
   - Runs FREE-WILi GUI firmware

### Why Our Arduino Code Didn't Show Anything

We successfully:
- ✅ Reconfigured PlatformIO for RP2350A (not ESP32)
- ✅ Fixed display dimensions to 320×240
- ✅ Built firmware (128KB flash, 11KB RAM)
- ✅ Uploaded via UF2 bootloader

But the display remained blank because:
- ❌ **The display is NOT directly connected to the Main Processor**
- ❌ **Direct TFT_eSPI library calls don't work**
- ❌ **Must communicate with Display Processor via serial protocol**

## Correct Approaches for Display Control

### Option 1: Python with FREE-WILi API (Recommended)

**Advantages:**
- Officially supported by FREE-WILi
- Complete API for display, buttons, sensors
- Runs from host computer
- Easy development and testing

**Setup:**
```bash
pip install freewili pillow result
python scripts/display_badge_design.py
```

**Files Created:**
- `scripts/display_badge_design.py` - Complete Python implementation

### Option 2: Arduino C++ with Serial Protocol

**Advantages:**
- Runs standalone on badge
- No host computer needed
- Lower latency

**Disadvantages:**
- Must implement FREE-WILi serial protocol
- Protocol not fully documented
- More complex development

**Would require:**
- Reverse-engineering the Display Processor protocol
- Implementing serial commands for display control
- Possible reference: freewili-python source code

### Option 3: Upload to Display Processor

**Advantages:**
- Direct hardware access to display
- Standard TFT_eSPI would work

**Disadvantages:**
- Would replace FREE-WILi GUI firmware
- Badge loses menu system functionality
- Harder to restore

## Hardware Specifications

### Display
- **Resolution:** 320×240 pixels (not 170×320!)
- **Driver:** Likely ST7789 or similar
- **Processor:** Separate RP2040 (Display Processor)
- **Control:** Via USB serial protocol from Main Processor

### Main Processor (RP2350A)
- **GPIO Header:** 20 pins (documented in FREE-WILi docs)
- **Interfaces:** SPI, I2C, UART, GPIO
- **Bootloader:** UF2 via RED button + USB
- **Framework:** Supports Arduino, MicroPython, CircuitPython

### Sensors & Peripherals
- 5 buttons (including RED for bootloader)
- 5 full-color LEDs
- BME688 gas sensor (pressure, humidity, temp)
- MQ-3 alcohol sensor
- XYZ position sensor
- IR transmit/receive
- Real-time clock (RTC)
- Speaker
- 1000mA lithium-ion battery with charger

## Pin Configuration Issues

Original code used ESP32 pins:
```cpp
MOSI=11, SCLK=12, CS=10, DC=13, RST=14, BL=9
```

These pins don't exist on the Main Processor's GPIO because:
- Display is on separate processor
- Display pins are internal to Display Processor
- Main Processor doesn't have direct display connections

## Correct Development Workflow

### For Display Applications:

1. **Use FREE-WILi Python API** (host-based)
   - Install: `pip install freewili`
   - Develop on host computer
   - Badge runs standard FREE-WILi firmware
   - Script communicates via USB serial

2. **Upload to Main Processor** (for GPIO/sensors)
   - Use RED button + USB for UF2 upload
   - Arduino/MicroPython/CircuitPython
   - Access: GPIO, sensors, buttons, LEDs
   - Display via serial commands to Display Processor

3. **Upload to Display Processor** (advanced, not recommended)
   - Use BLUE button + USB for UF2 upload
   - Replaces FREE-WILi GUI
   - Direct TFT_eSPI display access
   - Loses standard badge functionality

## Files Created

### Successful Arduino Build (Main Processor)
- `platformio.ini` - Configured for RP2350A
- `.pio/build/badge-test/firmware.uf2` - Compiled firmware (128KB)
- Uploaded successfully to Main Processor
- Runs but cannot control display without serial protocol

### Python Implementation (Recommended Approach)
- `scripts/display_badge_design.py` - Complete Python solution
- Uses FREE-WILi API for display control
- Generates .fwi image format
- Runs from host computer

### Documentation
- `BADGE_DESIGN_TEST.md` - Original test documentation (needs update)
- `scripts/README.md` - Scripts documentation
- `FINDINGS.md` - This document

## Next Steps

### To Display Badge Design:

1. **Install Python dependencies:**
   ```bash
   pip install freewili pillow result
   ```

2. **Ensure badge has FREE-WILi firmware:**
   - Display should show FREE-WILi menu when powered on
   - If not, download from: https://github.com/freewili/freewili-firmware

3. **Run the Python script:**
   ```bash
   cd badge_firmware/scripts
   python display_badge_design.py
   ```

### Alternative: Restore FREE-WILi Firmware

If the badge isn't showing the FREE-WILi menu:

1. Download Display Processor firmware (.uf2) from FREE-WILi GitHub
2. Hold BLUE button + plug USB
3. Drag .uf2 file to RP2350 drive
4. Badge will reboot with FREE-WILi GUI

## Resources

- FREE-WILi Documentation: https://docs.freewili.com/
- FREE-WILi Python API: https://github.com/freewili/freewili-python
- FREE-WILi Firmware: https://github.com/freewili/freewili-firmware
- GPIO Pinout: https://docs.freewili.com/gpio/gpio-pinout/
- ICS Village Badge: https://freewili.com/icsvillage-badge/

## Lessons Learned

1. **Always verify hardware architecture before coding**
   - Don't assume based on initial documentation
   - Look for multiple processors/modules
   - Check communication protocols

2. **Dual-processor badges are common at conferences**
   - One for UI/display
   - One for custom code/sensors
   - Communication via serial/I2C/SPI

3. **Use official APIs when available**
   - FREE-WILi provides complete Python API
   - Reverse-engineering protocols is time-consuming
   - Official support reduces debugging time

4. **Hardware identification is critical**
   - Original assumed: ESP32-S3 (LilyGo T-Display-S3)
   - Actual hardware: RP2350A + RP2040 dual-processor
   - Cost: Several hours of debugging

## Timeline Summary

- Initial code: Written for ESP32 (wrong architecture)
- First rewrite: RP2350A with direct display access (wrong approach)
- Final solution: Python + FREE-WILi API (correct approach)
- Total architecture discovery: ~2 hours
- Working solution: Python script ready to test

## Status

- ✅ Hardware architecture understood
- ✅ Correct firmware built and uploaded to Main Processor
- ✅ Python solution implemented
- ⏳ Pending: Install dependencies and test
- ⏳ Pending: Display badge design on screen

