# Badge Test Setup Guide

Author: David Broggy

## Quick Start - Get a Working Test in 3 Steps

### Step 1: Install Dependencies

```bash
# Create a virtual environment (avoids pip errors)
cd badge_firmware
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install freewili pillow result
```

### Step 2: Connect Your Badge

1. Plug the badge into USB
2. Verify it's connected:
   ```bash
   ls /dev/cu.usbmodem*
   # Should show: /dev/cu.usbmodem1401 (or similar)
   ```

3. Check the badge display:
   - Should show FREE-WILi menu
   - If blank, hold BLUE button + plug USB to restore firmware

### Step 3: Run Basic Test

```bash
python3 test_basic.py
```

**Expected output:**
```
==================================================
BASIC BADGE TEST
==================================================

[1/3] Importing freewili library...
✓ freewili imported successfully

[2/3] Searching for badge...
✓ Found 1 badge(s)
  Connected to: <device>

[3/3] Displaying test message...
✓ Text displayed successfully!

CHECK YOUR BADGE - You should see:
  'Hello World!'
  'Basic Test'
  'Working!'

==================================================
SUCCESS - Badge is working!
==================================================
```

**On your badge display, you should see:**
```
Hello World!

Basic Test
Working!
```

---

## Troubleshooting

### "freewili not installed"

**Solution:**
```bash
pip install freewili
```

Or use the virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install freewili result
```

### "No badges found"

**Check 1:** Is badge connected?
```bash
ls /dev/cu.usbmodem*
```

**Check 2:** Does badge show FREE-WILi menu?
- If NO: Badge needs FREE-WILi firmware
- Download from: https://github.com/freewili/freewili-firmware
- Upload using BLUE button + USB

**Check 3:** Try reconnecting
```bash
# Unplug badge
# Wait 3 seconds
# Plug back in
# Run test again
```

### "Could not configure port" or serial errors

**Solution:** Close other programs using the port
```bash
# Check what's using the port
lsof | grep usbmodem

# If screen or other tool is connected, exit it first
```

### Display stays blank

This means:
1. Badge doesn't have FREE-WILi firmware, OR
2. Badge is in bootloader mode

**Fix:**
1. Unplug badge
2. Plug back in normally (don't hold any buttons)
3. Wait for FREE-WILi menu to appear
4. Run test again

---

## What This Tests

- ✓ USB connection working
- ✓ Badge has FREE-WILi firmware
- ✓ Display Processor responding
- ✓ Text can be displayed
- ✓ Python API working

## Next Steps After Basic Test Works

Once you see "Hello World!" on your badge:

1. Test buttons: `python3 test_buttons.py` (to be created)
2. Test LEDs: `python3 test_leds.py` (to be created)
3. Display badge design: `python3 scripts/display_badge_design.py`

---

## Alternative: Test Without Python

If you want to test without installing Python packages:

1. Plug in badge
2. Open screen: `screen /dev/cu.usbmodem1401 115200`
3. The badge should respond to keypresses
4. Press Ctrl+A then K then Y to exit

This confirms USB serial is working.

---

## Files

- `test_basic.py` - Simple "Hello World" test
- `TEST_SETUP.md` - This file
- `FINDINGS.md` - Architecture documentation

---

## Important Notes

**The badge has TWO processors:**
1. Main Processor (RP2350A) - Runs your custom code
2. Display Processor (RP2040) - Controls the screen

**To program them:**
- Main: RED button + USB (UF2 files)
- Display: BLUE button + USB (UF2 files)

**For testing:**
- Keep FREE-WILi firmware on Display Processor
- Use Python API from your computer
- Simplest and most reliable approach

---

## Status Checklist

Before running tests, verify:

- [ ] Badge is plugged into USB
- [ ] `/dev/cu.usbmodem*` device exists
- [ ] Badge display shows FREE-WILi menu (not blank)
- [ ] Python 3.10+ installed
- [ ] `freewili` package installed (`pip list | grep freewili`)
- [ ] No other programs using the serial port

Once all checked, run: `python3 test_basic.py`
