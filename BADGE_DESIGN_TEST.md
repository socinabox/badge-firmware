# Badge Design Test

This test program displays the MVP Security Badge design on screen.

Author: David Broggy

## Three Ways to Run the Test

### Method 1: PlatformIO Separate Environment (Easiest - Recommended)

A dedicated build environment has been created so you can easily switch between test and main program.

**Run the badge design test:**
```bash
cd badge_firmware
pio run -e badge-test --target upload
```

**Run the main WiFi scanner program:**
```bash
pio run -e lilygo-t-display-s3 --target upload
```

No file renaming required! This is the cleanest approach.

### Method 2: FREE-WILi Scripts Menu (For ICS Village Badge)

If you're using the ICS Village badge with FREE-WILi GUI:

1. Connect badge via USB
2. Open FREE-WILi GUI application
3. Navigate to **Scripts** menu
4. Select **"Badge Design Test"**
5. Click **Run**

The Python script in `scripts/badge_design_test.py` will execute and display the badge design.

**Benefits:**
- No compilation required
- Easy to modify and test
- Works directly from the GUI
- Can run multiple scripts from menu

See `scripts/README.md` for more details on the scripts system.

### Method 3: Manual File Swapping (Legacy)

If you need to manually swap files:

```bash
cd badge_firmware/src
mv main.cpp main.cpp.backup
mv badge_design_test.cpp main.cpp
cd ..
pio run --target upload
```

**Restore main program:**
```bash
cd src
mv main.cpp badge_design_test.cpp
mv main.cpp.backup main.cpp
```

## What You'll See

Once the test runs, the badge design should appear on the display. The design includes:

- Shield outline with PCB aesthetic
- Circuit traces (vertical and horizontal lines)
- Circuit pads (small circles at connection points)
- Central lock icon with keyhole
- Unlocked key graphic
- Text: "MVP SUMMIT" and "2026"
- Binary code: "01010011 01000101 01000011" (SEC in binary)

## Troubleshooting

### Display is blank
- Check that the backlight is working (TFT_BL pin should be HIGH)
- Verify USB connection and power
- Check serial monitor for any error messages

### Colors look wrong
- The Azure Blue color (#00A4EF) is converted to RGB565 format (0x051F)
- If colors need adjustment, modify the AZURE_BLUE constant

### Design is cut off or doesn't fit
- The design is automatically scaled from the original 3450x3450 SVG to fit the 170x320 display
- Adjust the scale calculation in drawBadgeDesign() if needed

## Customization

You can modify the badge design by editing `badge_design_test.cpp`:

- **Change colors**: Modify the `AZURE_BLUE` constant
- **Adjust scaling**: Modify the scale calculation in `drawBadgeDesign()`
- **Add elements**: Use TFT_eSPI drawing functions (drawLine, drawCircle, fillRect, etc.)

## Serial Monitor

Open the serial monitor at 115200 baud to see debug output:

```bash
pio device monitor
```

Author: David Broggy
