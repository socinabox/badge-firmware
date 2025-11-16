#ifndef CONFIG_H
#define CONFIG_H

// Badge Configuration
#define BADGE_ID "MVP-BADGE-001"
#define FIRMWARE_VERSION "1.0.0"

// WiFi Configuration for API Upload
#define WIFI_SSID "YOUR_WIFI_SSID"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

// Azure Function API Configuration
#define API_ENDPOINT "https://YOUR_FUNCTION_APP.azurewebsites.net/api/badge-data"
#define API_KEY "YOUR_FUNCTION_KEY"

// Display Configuration - ICS Village Badge (320x240)
#define SCREEN_WIDTH 240
#define SCREEN_HEIGHT 320
#define DISPLAY_ROTATION 0  // 0, 1, 2, or 3

// WiFi Sniffer Configuration
#define MAX_NETWORKS 100
#define CHANNEL_HOP_INTERVAL_MS 200  // Time on each channel
#define SCAN_ALL_CHANNELS true
#define START_CHANNEL 1
#define END_CHANNEL 13  // 14 for Japan

// Upload Configuration
#define UPLOAD_INTERVAL_MS 30000  // Upload every 30 seconds
#define MAX_UPLOAD_RETRIES 3

// Display Modes
#define DISPLAY_MODE_3D_BARS 0
#define DISPLAY_MODE_WAVES 1
#define DISPLAY_MODE_RADIAL 2
#define DISPLAY_MODE_LIST 3

// Button GPIO Pins (T-Display-S3)
#define BUTTON_1 0   // Boot button
#define BUTTON_2 14  // Secondary button

// Battery Monitoring
#define BATTERY_PIN 4
#define BATTERY_VOLTAGE_DIVIDER 2.0

// Power Saving
#define ENABLE_POWER_SAVING true
#define SLEEP_AFTER_INACTIVITY_MS 300000  // 5 minutes

#endif // CONFIG_H
