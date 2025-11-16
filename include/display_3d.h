#ifndef DISPLAY_3D_H
#define DISPLAY_3D_H

#include <TFT_eSPI.h>
#include "wifi_sniffer.h"

class Display3D {
public:
    Display3D(TFT_eSPI* tft);
    void begin();
    void update(WiFiNetwork* networks, int count);
    void setMode(uint8_t mode);
    uint8_t getMode();
    void drawStatusBar(int networkCount, float batteryVoltage, bool uploading);

private:
    TFT_eSPI* tft;
    uint8_t displayMode;
    unsigned long lastUpdate;
    float animationPhase;

    // Display mode renderers
    void draw3DBars(WiFiNetwork* networks, int count);
    void drawWaves(WiFiNetwork* networks, int count);
    void drawRadial(WiFiNetwork* networks, int count);
    void drawList(WiFiNetwork* networks, int count);

    // Helper functions
    void drawBar3D(int x, int y, int width, int height, uint16_t color, int depth);
    void drawWaveLine(int* points, int numPoints, uint16_t color);
    uint16_t getColorForRSSI(int8_t rssi);
    uint16_t getColorForEncryption(uint8_t encryption);
    void drawText(const char* text, int x, int y, uint8_t font);

    // 3D Math helpers
    struct Point3D {
        float x, y, z;
    };
    struct Point2D {
        int x, y;
    };
    Point2D project3D(Point3D point);
};

#endif // DISPLAY_3D_H
