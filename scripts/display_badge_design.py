"""
MVP Security Badge - Display Badge Design via FREE-WILi API

This script uses the FREE-WILi Python library to display the badge design
by communicating with the badge's Display Processor via USB serial.

Author: David Broggy

Requirements:
    pip install freewili pillow

Usage:
    python display_badge_design.py
"""

import sys
from pathlib import Path
from freewili import find_freewilis
from freewili.fw import FreeWili
from result import Ok, Err
from PIL import Image, ImageDraw, ImageFont

# Display configuration - ICS Village Badge
SCREEN_WIDTH = 240
SCREEN_HEIGHT = 320

# Color - Microsoft Azure Blue
AZURE_BLUE_RGB = (0, 164, 239)  # #00A4EF


def create_badge_design_image():
    """Create the MVP Security Badge design as a PIL Image."""
    # Create image with black background
    img = Image.new('RGB', (SCREEN_WIDTH, SCREEN_HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Calculate scaling factors to fit 3450x3450 SVG into 240x320 display
    scale = SCREEN_WIDTH / 3450.0
    offset_x = 0
    offset_y = (SCREEN_HEIGHT - int(3450 * scale)) // 2

    # Helper functions to scale coordinates
    def sx(x):
        return int(x * scale) + offset_x

    def sy(y):
        return int(y * scale) + offset_y

    def ss(s):
        return max(1, int(s * scale))

    # Draw main shield outline
    draw.line([sx(1725), sy(200), sx(2800), sy(600)], fill=AZURE_BLUE_RGB, width=2)
    draw.line([sx(2800), sy(600), sx(2800), sy(1800)], fill=AZURE_BLUE_RGB, width=2)
    draw.line([sx(1725), sy(200), sx(650), sy(600)], fill=AZURE_BLUE_RGB, width=2)
    draw.line([sx(650), sy(600), sx(650), sy(1800)], fill=AZURE_BLUE_RGB, width=2)

    # Draw bottom curves (approximated with lines)
    for i in range(10):
        x1 = 650 + i * 200
        y1 = 1800 + i * 100
        x2 = 650 + (i + 1) * 200
        y2 = 1800 + (i + 1) * 100
        draw.line([sx(x1), sy(y1), sx(x2), sy(y2)], fill=AZURE_BLUE_RGB, width=2)

    for i in range(10):
        x1 = 2800 - i * 200
        y1 = 1800 + i * 100
        x2 = 2800 - (i + 1) * 200
        y2 = 1800 + (i + 1) * 100
        draw.line([sx(x1), sy(y1), sx(x2), sy(y2)], fill=AZURE_BLUE_RGB, width=2)

    # Draw circuit traces - vertical lines
    draw.line([sx(1000), sy(700), sx(1000), sy(2200)], fill=AZURE_BLUE_RGB, width=1)
    draw.line([sx(1400), sy(800), sx(1400), sy(2400)], fill=AZURE_BLUE_RGB, width=1)
    draw.line([sx(2050), sy(800), sx(2050), sy(2400)], fill=AZURE_BLUE_RGB, width=1)
    draw.line([sx(2450), sy(700), sx(2450), sy(2200)], fill=AZURE_BLUE_RGB, width=1)

    # Draw circuit traces - horizontal connections
    draw.line([sx(900), sy(1000), sx(2550), sy(1000)], fill=AZURE_BLUE_RGB, width=1)
    draw.line([sx(950), sy(1300), sx(2500), sy(1300)], fill=AZURE_BLUE_RGB, width=1)
    draw.line([sx(1000), sy(1900), sx(2450), sy(1900)], fill=AZURE_BLUE_RGB, width=1)

    # Draw circuit pads (small circles)
    r = ss(25)
    draw.ellipse([sx(1000)-r, sy(1000)-r, sx(1000)+r, sy(1000)+r], fill=AZURE_BLUE_RGB)
    r = ss(20)
    draw.ellipse([sx(1200)-r, sy(1000)-r, sx(1200)+r, sy(1000)+r], fill=AZURE_BLUE_RGB)
    draw.ellipse([sx(2250)-r, sy(1000)-r, sx(2250)+r, sy(1000)+r], fill=AZURE_BLUE_RGB)
    r = ss(25)
    draw.ellipse([sx(2450)-r, sy(1000)-r, sx(2450)+r, sy(1000)+r], fill=AZURE_BLUE_RGB)

    # Draw central lock icon
    draw.rectangle([sx(1600), sy(1450), sx(1850), sy(1750)], outline=AZURE_BLUE_RGB, width=2)
    r = ss(80)
    draw.ellipse([sx(1725)-r, sy(1380)-r, sx(1725)+r, sy(1380)+r], outline=AZURE_BLUE_RGB, width=2)
    draw.line([sx(1645), sy(1380), sx(1645), sy(1450)], fill=AZURE_BLUE_RGB, width=2)
    draw.line([sx(1805), sy(1380), sx(1805), sy(1450)], fill=AZURE_BLUE_RGB, width=2)

    # Draw keyhole
    r = ss(30)
    draw.ellipse([sx(1725)-r, sy(1580)-r, sx(1725)+r, sy(1580)+r], fill=AZURE_BLUE_RGB)
    draw.rectangle([sx(1710), sy(1580), sx(1740), sy(1660)], fill=AZURE_BLUE_RGB)

    # Draw unlocked key
    r = ss(35)
    draw.ellipse([sx(2100)-r, sy(1600)-r, sx(2100)+r, sy(1600)+r], outline=AZURE_BLUE_RGB, width=2)
    draw.line([sx(2135), sy(1600), sx(2250), sy(1600)], fill=AZURE_BLUE_RGB, width=2)

    # Draw corner circuit elements
    r = ss(30)
    draw.ellipse([sx(900)-r, sy(800)-r, sx(900)+r, sy(800)+r], fill=AZURE_BLUE_RGB)
    draw.ellipse([sx(2550)-r, sy(800)-r, sx(2550)+r, sy(800)+r], fill=AZURE_BLUE_RGB)

    # Draw diagonal circuit traces
    draw.line([sx(900), sy(800), sx(1000), sy(1000)], fill=AZURE_BLUE_RGB, width=1)
    draw.line([sx(2550), sy(800), sx(2450), sy(1000)], fill=AZURE_BLUE_RGB, width=1)

    # Draw top antenna
    r = ss(40)
    draw.ellipse([sx(1725)-r, sy(200)-r, sx(1725)+r, sy(200)+r], fill=AZURE_BLUE_RGB)
    draw.line([sx(1725), sy(240), sx(1725), sy(300)], fill=AZURE_BLUE_RGB, width=2)

    # Draw side connection points
    r = ss(35)
    draw.ellipse([sx(2800)-r, sy(1200)-r, sx(2800)+r, sy(1200)+r], fill=AZURE_BLUE_RGB)
    draw.ellipse([sx(650)-r, sy(1200)-r, sx(650)+r, sy(1200)+r], fill=AZURE_BLUE_RGB)

    # Draw text
    try:
        # Try to use a nice font, fall back to default if not available
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
        font_tiny = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 8)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_tiny = ImageFont.load_default()

    # Center text
    text1 = "MVP SUMMIT"
    text2 = "2026"
    text3 = "01010011 01000101 01000011"  # SEC in binary

    bbox1 = draw.textbbox((0, 0), text1, font=font_large)
    bbox2 = draw.textbbox((0, 0), text2, font=font_large)
    bbox3 = draw.textbbox((0, 0), text3, font=font_tiny)

    w1 = bbox1[2] - bbox1[0]
    w2 = bbox2[2] - bbox2[0]
    w3 = bbox3[2] - bbox3[0]

    draw.text(((SCREEN_WIDTH - w1) // 2, sy(2600)), text1, fill=AZURE_BLUE_RGB, font=font_large)
    draw.text(((SCREEN_WIDTH - w2) // 2, sy(2800)), text2, fill=AZURE_BLUE_RGB, font=font_large)
    draw.text(((SCREEN_WIDTH - w3) // 2, sy(2950)), text3, fill=AZURE_BLUE_RGB, font=font_tiny)

    return img


def main():
    """Main entry point."""
    print("=" * 50)
    print("MVP Security Badge - Display Badge Design")
    print("=" * 50)

    # Find connected FREE-WILi badges
    print("\n[1/4] Searching for FREE-WILi badges...")
    fws = find_freewilis()

    if not fws:
        print("ERROR: No FREE-WILi badges found!")
        print("Make sure your badge is connected via USB.")
        return 1

    print(f"Found {len(fws)} badge(s)")

    # Use the first badge found
    fw = FreeWili(fws[0])
    print(f"Using badge: {fws[0]}")

    # Create the badge design image
    print("\n[2/4] Creating badge design image...")
    img = create_badge_design_image()

    # Save temporarily
    temp_image = Path("/tmp/badge_design.png")
    img.save(temp_image)
    print(f"Image created: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

    # Convert to FREE-WILi format
    print("\n[3/4] Converting to FREE-WILi format...")
    temp_fwi = Path("/tmp/badge_design.fwi")

    from freewili.image import convert
    result = convert(temp_image, temp_fwi)

    match result:
        case Ok(msg):
            print(f"Success: {msg}")
        case Err(msg):
            print(f"ERROR: {msg}")
            return 1

    # Display on badge
    print("\n[4/4] Sending to badge display...")

    # First show a text message
    result = fw.show_text_display("MVP Security Badge\nDesign Loading...")
    match result:
        case Ok(_):
            print("Text displayed successfully")
        case Err(msg):
            print(f"Warning: Could not display text: {msg}")

    import time
    time.sleep(1)

    # TODO: Add image display command when available in API
    # For now, the badge design image is ready at /tmp/badge_design.fwi

    print("\n" + "=" * 50)
    print("SUCCESS!")
    print("Badge design image created at:", temp_fwi)
    print("\nNote: Image display API may require firmware update")
    print("or manual upload via FREE-WILi GUI")
    print("=" * 50)

    return 0


if __name__ == "__main__":
    sys.exit(main())
