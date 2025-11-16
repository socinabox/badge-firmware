# Badge Scripts

This folder contains scripts that can be executed from the badge UI or FREE-WILi interface.

Author: David Broggy

## Scripts Overview

### badge_design_test.py

Displays the MVP Security Badge design on the screen.

- **Type:** Python
- **Category:** Test
- **Purpose:** Verify badge design rendering and display functionality

**Features:**

- Renders shield outline with PCB aesthetic
- Displays circuit traces and connection pads
- Shows lock icon and security elements
- Text: "MVP SUMMIT 2026"
- Binary code easter egg

## Usage

### Option 1: FREE-WILi GUI (Recommended)

If you have the FREE-WILi GUI application installed:

1. Connect badge via USB
2. Open FREE-WILi
3. Navigate to Scripts menu
4. Select "Badge Design Test"
5. Click Run

The script will automatically load and display the badge design.

### Option 2: Direct Upload via USB Serial

```bash
# Copy script to badge
python -m serial.tools.miniterm /dev/cu.usbmodem* 115200

# In the badge console:
>>> import badge_design_test
>>> badge_design_test.main()
```

### Option 3: PlatformIO (For Compiled Version)

If you prefer the compiled C++ version:

```bash
cd ..
pio run -e badge-test --target upload
```

## Adding New Scripts

To add a new script to the menu:

1. Create your Python script in this folder
2. Add entry to `menu.json`:

```json
{
  "id": "your_script_id",
  "name": "Your Script Name",
  "description": "What your script does",
  "file": "your_script.py",
  "type": "python",
  "category": "test",
  "icon": "icon_name"
}
```

3. Reload scripts in FREE-WILi

## Script API Reference

Scripts have access to the badge API:

### Display Functions

```python
display.fill(color)                      # Fill screen with color
display.line(x1, y1, x2, y2, color)     # Draw line
display.rect(x, y, w, h, color)         # Draw rectangle
display.fill_rect(x, y, w, h, color)    # Draw filled rectangle
display.circle(x, y, r, color)          # Draw circle
display.fill_circle(x, y, r, color)     # Draw filled circle
display.text(text, x, y, color)         # Draw text
display.text_center(text, x, y)         # Draw centered text
display.show()                           # Update display
```

### Button Functions

```python
badge.button_pressed()                   # Check if any button pressed
badge.button_pressed(button_id)         # Check specific button
```

### LED Functions

```python
badge.led_set(led_id, color)            # Set LED color (RGB)
badge.led_off(led_id)                   # Turn off LED
```

### Sensor Functions

```python
badge.sensor.temperature()              # Read temperature
badge.sensor.humidity()                 # Read humidity
badge.sensor.pressure()                 # Read pressure
```

## Colors (RGB565 Format)

Common colors for badge scripts:

- Azure Blue: `0x051F` (#00A4EF - Microsoft Azure)
- Black: `0x0000`
- White: `0xFFFF`
- Red: `0xF800`
- Green: `0x07E0`
- Blue: `0x001F`

## Directory Structure

```
scripts/
├── README.md                  # This file
├── menu.json                  # Script menu configuration
├── badge_design_test.py       # Badge design test script
└── [your_scripts.py]          # Add your scripts here
```

## Troubleshooting

### Script not appearing in FREE-WILi

- Check that `menu.json` is properly formatted
- Verify script file exists in this directory
- Reload scripts in FREE-WILi

### Display not working

- Verify badge is connected
- Check display initialization
- Try the compiled C++ version instead

### Import errors

- Ensure badge Python environment is set up
- Check that required modules are available
- Try running from FREE-WILi instead of direct serial

## Resources

- FREE-WILi Documentation: https://freewili.com/docs/
- Badge API Reference: https://freewili.com/docs/api/
- Python Examples: https://freewili.com/docs/examples/
