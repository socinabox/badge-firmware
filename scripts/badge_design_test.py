"""
MVP Security Badge - Design Test Script
Displays the badge design on screen

This script can be run from FREE-WILi or directly on the badge.
Compatible with ICS Village badge or similar hardware.

Author: David Broggy
"""

# Display configuration
SCREEN_WIDTH = 170
SCREEN_HEIGHT = 320

# Color - Microsoft Azure Blue (RGB565: 0x051F for #00A4EF)
AZURE_BLUE = 0x051F
BLACK = 0x0000

def scale_x(x, scale, offset_x=0):
    """Scale X coordinate from 3450x3450 SVG space to display space"""
    return int(x * scale) + offset_x

def scale_y(y, scale, offset_y=0):
    """Scale Y coordinate from 3450x3450 SVG space to display space"""
    return int(y * scale) + offset_y

def scale_size(s, scale):
    """Scale size dimension"""
    return max(1, int(s * scale))

def draw_badge_design(display):
    """Draw the MVP Security Badge design scaled to fit the display"""

    # Clear screen
    display.fill(BLACK)

    # Calculate scaling factors to fit 3450x3450 SVG into display
    # Center it and scale to fit width
    scale = SCREEN_WIDTH / 3450.0
    offset_x = 0
    offset_y = (SCREEN_HEIGHT - int(3450 * scale)) // 2

    # Helper functions with closure over scale and offsets
    sx = lambda x: scale_x(x, scale, offset_x)
    sy = lambda y: scale_y(y, scale, offset_y)
    ss = lambda s: scale_size(s, scale)

    # Draw main shield outline
    display.line(sx(1725), sy(200), sx(2800), sy(600), AZURE_BLUE)
    display.line(sx(2800), sy(600), sx(2800), sy(1800), AZURE_BLUE)
    display.line(sx(1725), sy(200), sx(650), sy(600), AZURE_BLUE)
    display.line(sx(650), sy(600), sx(650), sy(1800), AZURE_BLUE)

    # Draw bottom curves (approximated with line segments)
    for i in range(10):
        x1 = 650 + i * 200
        y1 = 1800 + i * 100
        x2 = 650 + (i + 1) * 200
        y2 = 1800 + (i + 1) * 100
        display.line(sx(x1), sy(y1), sx(x2), sy(y2), AZURE_BLUE)

    for i in range(10):
        x1 = 2800 - i * 200
        y1 = 1800 + i * 100
        x2 = 2800 - (i + 1) * 200
        y2 = 1800 + (i + 1) * 100
        display.line(sx(x1), sy(y1), sx(x2), sy(y2), AZURE_BLUE)

    # Draw circuit traces - vertical lines
    display.line(sx(1000), sy(700), sx(1000), sy(2200), AZURE_BLUE)
    display.line(sx(1400), sy(800), sx(1400), sy(2400), AZURE_BLUE)
    display.line(sx(2050), sy(800), sx(2050), sy(2400), AZURE_BLUE)
    display.line(sx(2450), sy(700), sx(2450), sy(2200), AZURE_BLUE)

    # Draw circuit traces - horizontal connections
    display.line(sx(900), sy(1000), sx(2550), sy(1000), AZURE_BLUE)
    display.line(sx(950), sy(1300), sx(2500), sy(1300), AZURE_BLUE)
    display.line(sx(1000), sy(1900), sx(2450), sy(1900), AZURE_BLUE)

    # Draw circuit pads (small circles)
    display.fill_circle(sx(1000), sy(1000), ss(25), AZURE_BLUE)
    display.fill_circle(sx(1200), sy(1000), ss(20), AZURE_BLUE)
    display.fill_circle(sx(2250), sy(1000), ss(20), AZURE_BLUE)
    display.fill_circle(sx(2450), sy(1000), ss(25), AZURE_BLUE)

    # Draw central lock icon
    display.rect(sx(1600), sy(1450), ss(250), ss(300), AZURE_BLUE)
    display.circle(sx(1725), sy(1380), ss(80), AZURE_BLUE)
    display.line(sx(1645), sy(1380), sx(1645), sy(1450), AZURE_BLUE)
    display.line(sx(1805), sy(1380), sx(1805), sy(1450), AZURE_BLUE)

    # Draw keyhole
    display.fill_circle(sx(1725), sy(1580), ss(30), AZURE_BLUE)
    display.fill_rect(sx(1710), sy(1580), ss(30), ss(80), AZURE_BLUE)

    # Draw unlocked key
    display.circle(sx(2100), sy(1600), ss(35), AZURE_BLUE)
    display.line(sx(2135), sy(1600), sx(2250), sy(1600), AZURE_BLUE)

    # Draw corner circuit elements
    display.fill_circle(sx(900), sy(800), ss(30), AZURE_BLUE)
    display.fill_circle(sx(2550), sy(800), ss(30), AZURE_BLUE)

    # Draw diagonal circuit traces
    display.line(sx(900), sy(800), sx(1000), sy(1000), AZURE_BLUE)
    display.line(sx(2550), sy(800), sx(2450), sy(1000), AZURE_BLUE)

    # Draw top antenna
    display.fill_circle(sx(1725), sy(200), ss(40), AZURE_BLUE)
    display.line(sx(1725), sy(240), sx(1725), sy(300), AZURE_BLUE)

    # Draw side connection points
    display.fill_circle(sx(2800), sy(1200), ss(35), AZURE_BLUE)
    display.fill_circle(sx(650), sy(1200), ss(35), AZURE_BLUE)

    # Draw text
    display.set_text_color(AZURE_BLUE, BLACK)
    display.text_center("MVP SUMMIT", SCREEN_WIDTH // 2, sy(2600))
    display.text_center("2026", SCREEN_WIDTH // 2, sy(2800))
    display.text_center("01010011 01000101 01000011", SCREEN_WIDTH // 2, sy(2950), size=1)

    # Update display
    display.show()

def main():
    """Main entry point for the script"""
    try:
        # Import badge display module (will vary by platform)
        # This is a generic interface - adapt to your specific badge
        import badge

        print("=" * 40)
        print("Badge Design Test")
        print("=" * 40)
        print("Drawing MVP Security Badge design...")

        # Get display object
        display = badge.display

        # Draw the badge
        draw_badge_design(display)

        print("Badge design displayed!")
        print("Press any button to exit")

        # Wait for button press
        while True:
            if badge.button_pressed():
                break

    except ImportError:
        print("ERROR: Badge module not found")
        print("This script requires badge hardware support")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
