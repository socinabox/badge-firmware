#include <Arduino.h>
#include <TFT_eSPI.h>

// Display dimensions - ICS Village Badge
#define SCREEN_WIDTH 240
#define SCREEN_HEIGHT 320

// Color - Microsoft Azure Blue
#define AZURE_BLUE 0x051F  // RGB565 format for #00A4EF

TFT_eSPI tft = TFT_eSPI();

// Function to draw the badge design scaled to fit the display
void drawBadgeDesign() {
    // Clear screen
    tft.fillScreen(TFT_BLACK);

    // Calculate scaling factors to fit 3450x3450 SVG into 240x320 display
    // We'll center it and scale to fit width
    float scale = SCREEN_WIDTH / 3450.0;
    int offsetX = 0;
    int offsetY = (SCREEN_HEIGHT - (int)(3450 * scale)) / 2;

    // Helper function to scale coordinates
    auto scaleX = [scale, offsetX](int x) { return (int)(x * scale) + offsetX; };
    auto scaleY = [scale, offsetY](int y) { return (int)(y * scale) + offsetY; };
    auto scaleSize = [scale](int s) { return max(1, (int)(s * scale)); };

    // Draw main shield outline
    tft.drawLine(scaleX(1725), scaleY(200), scaleX(2800), scaleY(600), AZURE_BLUE);
    tft.drawLine(scaleX(2800), scaleY(600), scaleX(2800), scaleY(1800), AZURE_BLUE);
    tft.drawLine(scaleX(1725), scaleY(200), scaleX(650), scaleY(600), AZURE_BLUE);
    tft.drawLine(scaleX(650), scaleY(600), scaleX(650), scaleY(1800), AZURE_BLUE);

    // Draw bottom curves (approximated with lines)
    for (int i = 0; i < 10; i++) {
        int x1 = 650 + i * 200;
        int y1 = 1800 + i * 100;
        int x2 = 650 + (i + 1) * 200;
        int y2 = 1800 + (i + 1) * 100;
        tft.drawLine(scaleX(x1), scaleY(y1), scaleX(x2), scaleY(y2), AZURE_BLUE);
    }
    for (int i = 0; i < 10; i++) {
        int x1 = 2800 - i * 200;
        int y1 = 1800 + i * 100;
        int x2 = 2800 - (i + 1) * 200;
        int y2 = 1800 + (i + 1) * 100;
        tft.drawLine(scaleX(x1), scaleY(y1), scaleX(x2), scaleY(y2), AZURE_BLUE);
    }

    // Draw circuit traces - vertical lines
    tft.drawLine(scaleX(1000), scaleY(700), scaleX(1000), scaleY(2200), AZURE_BLUE);
    tft.drawLine(scaleX(1400), scaleY(800), scaleX(1400), scaleY(2400), AZURE_BLUE);
    tft.drawLine(scaleX(2050), scaleY(800), scaleX(2050), scaleY(2400), AZURE_BLUE);
    tft.drawLine(scaleX(2450), scaleY(700), scaleX(2450), scaleY(2200), AZURE_BLUE);

    // Draw circuit traces - horizontal connections
    tft.drawLine(scaleX(900), scaleY(1000), scaleX(2550), scaleY(1000), AZURE_BLUE);
    tft.drawLine(scaleX(950), scaleY(1300), scaleX(2500), scaleY(1300), AZURE_BLUE);
    tft.drawLine(scaleX(1000), scaleY(1900), scaleX(2450), scaleY(1900), AZURE_BLUE);

    // Draw circuit pads (small circles)
    tft.fillCircle(scaleX(1000), scaleY(1000), scaleSize(25), AZURE_BLUE);
    tft.fillCircle(scaleX(1200), scaleY(1000), scaleSize(20), AZURE_BLUE);
    tft.fillCircle(scaleX(2250), scaleY(1000), scaleSize(20), AZURE_BLUE);
    tft.fillCircle(scaleX(2450), scaleY(1000), scaleSize(25), AZURE_BLUE);

    // Draw central lock icon
    tft.drawRect(scaleX(1600), scaleY(1450), scaleSize(250), scaleSize(300), AZURE_BLUE);
    tft.drawCircle(scaleX(1725), scaleY(1380), scaleSize(80), AZURE_BLUE);
    tft.drawLine(scaleX(1645), scaleY(1380), scaleX(1645), scaleY(1450), AZURE_BLUE);
    tft.drawLine(scaleX(1805), scaleY(1380), scaleX(1805), scaleY(1450), AZURE_BLUE);

    // Draw keyhole
    tft.fillCircle(scaleX(1725), scaleY(1580), scaleSize(30), AZURE_BLUE);
    tft.fillRect(scaleX(1710), scaleY(1580), scaleSize(30), scaleSize(80), AZURE_BLUE);

    // Draw unlocked key
    tft.drawCircle(scaleX(2100), scaleY(1600), scaleSize(35), AZURE_BLUE);
    tft.drawLine(scaleX(2135), scaleY(1600), scaleX(2250), scaleY(1600), AZURE_BLUE);

    // Draw corner circuit elements
    tft.fillCircle(scaleX(900), scaleY(800), scaleSize(30), AZURE_BLUE);
    tft.fillCircle(scaleX(2550), scaleY(800), scaleSize(30), AZURE_BLUE);

    // Draw diagonal circuit traces
    tft.drawLine(scaleX(900), scaleY(800), scaleX(1000), scaleY(1000), AZURE_BLUE);
    tft.drawLine(scaleX(2550), scaleY(800), scaleX(2450), scaleY(1000), AZURE_BLUE);

    // Draw top antenna
    tft.fillCircle(scaleX(1725), scaleY(200), scaleSize(40), AZURE_BLUE);
    tft.drawLine(scaleX(1725), scaleY(240), scaleX(1725), scaleY(300), AZURE_BLUE);

    // Draw side connection points
    tft.fillCircle(scaleX(2800), scaleY(1200), scaleSize(35), AZURE_BLUE);
    tft.fillCircle(scaleX(650), scaleY(1200), scaleSize(35), AZURE_BLUE);

    // Draw text - MVP SUMMIT
    tft.setTextColor(AZURE_BLUE, TFT_BLACK);
    tft.setTextDatum(MC_DATUM);
    tft.setTextSize(1);
    tft.drawString("MVP SUMMIT", SCREEN_WIDTH/2, scaleY(2600), 4);

    // Draw text - 2026
    tft.drawString("2026", SCREEN_WIDTH/2, scaleY(2800), 4);

    // Draw binary code (smaller font)
    tft.drawString("01010011 01000101 01000011", SCREEN_WIDTH/2, scaleY(2950), 1);
}

void setup() {
    Serial.begin(115200);
    delay(1000);

    Serial.println("=================================");
    Serial.println("Badge Design Test");
    Serial.println("=================================");

    // Initialize display
    tft.init();
    tft.setRotation(0);  // Portrait mode
    tft.fillScreen(TFT_BLACK);

    // Set backlight
    pinMode(TFT_BL, OUTPUT);
    digitalWrite(TFT_BL, HIGH);

    Serial.println("Drawing badge design...");

    // Draw the badge
    drawBadgeDesign();

    Serial.println("Badge design displayed!");
    Serial.println("Press RESET to redraw");
}

void loop() {
    // Nothing to do in loop - badge is static
    delay(1000);
}
