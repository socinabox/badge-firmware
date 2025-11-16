#include <Arduino.h>
#include <TFT_eSPI.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "config.h"
#include "wifi_sniffer.h"
#include "display_3d.h"

// Global objects
TFT_eSPI tft = TFT_eSPI();
WiFiSniffer* sniffer;
Display3D* display3d;

// State variables
bool scanning = false;
unsigned long lastUpload = 0;
unsigned long lastButtonCheck = 0;
uint8_t displayMode = DISPLAY_MODE_3D_BARS;
float batteryVoltage = 0.0;
bool uploading = false;

// Forward declarations
void setupDisplay();
void setupButtons();
void handleButtons();
float readBatteryVoltage();
void uploadData();
String generateJSON();
void switchToStationMode();
void switchToMonitorMode();

void setup() {
    Serial.begin(115200);
    delay(1000);

    Serial.println("=================================");
    Serial.println("MVP Security Badge - WiFi Monitor");
    Serial.println("=================================");
    Serial.printf("Badge ID: %s\n", BADGE_ID);
    Serial.printf("Firmware: %s\n", FIRMWARE_VERSION);
    Serial.println();

    // Initialize display
    setupDisplay();
    tft.fillScreen(TFT_BLACK);
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.setTextDatum(MC_DATUM);
    tft.drawString("MVP SECURITY BADGE", SCREEN_WIDTH/2, 40, 4);
    tft.drawString("Initializing...", SCREEN_WIDTH/2, 80, 2);

    // Initialize WiFi sniffer
    Serial.println("[+] Initializing WiFi sniffer...");
    sniffer = new WiFiSniffer(MAX_NETWORKS);
    sniffer->begin();

    // Initialize 3D display
    Serial.println("[+] Initializing 3D display...");
    display3d = new Display3D(&tft);
    display3d->begin();
    display3d->setMode(displayMode);

    // Setup buttons
    setupButtons();

    // Show ready screen
    delay(1000);
    tft.fillScreen(TFT_BLACK);
    tft.drawString("READY", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 4);
    tft.drawString("Press BTN1 to start", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 40, 2);

    Serial.println("[+] Badge initialized");
    Serial.println("[+] Press button 1 to start scanning");
}

void loop() {
    unsigned long currentMillis = millis();

    // Handle button presses
    if (currentMillis - lastButtonCheck >= 50) {
        handleButtons();
        lastButtonCheck = currentMillis;
    }

    // Update scanner if active
    if (scanning) {
        sniffer->update();

        // Update display
        int networkCount = sniffer->getNetworkCount();
        WiFiNetwork* networks = sniffer->getAllNetworks();
        display3d->update(networks, networkCount);
        display3d->drawStatusBar(networkCount, batteryVoltage, uploading);

        // Upload data periodically
        if (currentMillis - lastUpload >= UPLOAD_INTERVAL_MS) {
            uploadData();
            lastUpload = currentMillis;
        }
    }

    // Read battery voltage periodically
    if (currentMillis % 5000 == 0) {
        batteryVoltage = readBatteryVoltage();
    }

    delay(10);  // Small delay to prevent watchdog
}

void setupDisplay() {
    tft.init();
    tft.setRotation(DISPLAY_ROTATION);
    tft.fillScreen(TFT_BLACK);

    // Set backlight
    pinMode(TFT_BL, OUTPUT);
    digitalWrite(TFT_BL, HIGH);
}

void setupButtons() {
    pinMode(BUTTON_1, INPUT_PULLUP);
    pinMode(BUTTON_2, INPUT_PULLUP);
}

void handleButtons() {
    static bool button1Pressed = false;
    static bool button2Pressed = false;

    // Button 1: Start/Stop scanning
    if (digitalRead(BUTTON_1) == LOW && !button1Pressed) {
        button1Pressed = true;
        scanning = !scanning;

        if (scanning) {
            Serial.println("[+] Starting WiFi scanning...");
            sniffer->start();
            tft.fillScreen(TFT_BLACK);
        } else {
            Serial.println("[+] Stopping WiFi scanning...");
            sniffer->stop();
            tft.fillScreen(TFT_BLACK);
            tft.setTextDatum(MC_DATUM);
            tft.drawString("PAUSED", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 4);
        }
    } else if (digitalRead(BUTTON_1) == HIGH) {
        button1Pressed = false;
    }

    // Button 2: Cycle display modes
    if (digitalRead(BUTTON_2) == LOW && !button2Pressed && scanning) {
        button2Pressed = true;
        displayMode = (displayMode + 1) % 4;
        display3d->setMode(displayMode);

        const char* modes[] = {"3D Bars", "Waves", "Radial", "List"};
        Serial.printf("[+] Display mode: %s\n", modes[displayMode]);
    } else if (digitalRead(BUTTON_2) == HIGH) {
        button2Pressed = false;
    }
}

float readBatteryVoltage() {
    int rawValue = analogRead(BATTERY_PIN);
    float voltage = (rawValue / 4095.0) * 3.3 * BATTERY_VOLTAGE_DIVIDER;
    return voltage;
}

void uploadData() {
    if (!scanning) return;

    int networkCount = sniffer->getNetworkCount();
    if (networkCount == 0) {
        Serial.println("[!] No networks to upload");
        return;
    }

    Serial.printf("[*] Uploading %d networks to Azure...\n", networkCount);
    uploading = true;

    // Switch to station mode for upload
    sniffer->stop();
    switchToStationMode();

    // Connect to WiFi
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    int retries = 0;
    while (WiFi.status() != WL_CONNECTED && retries < 20) {
        delay(500);
        Serial.print(".");
        retries++;
    }

    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\n[+] Connected to WiFi");

        // Prepare JSON payload
        String jsonPayload = generateJSON();

        // Send HTTP POST
        HTTPClient http;
        http.begin(API_ENDPOINT);
        http.addHeader("Content-Type", "application/json");
        http.addHeader("x-functions-key", API_KEY);

        int httpResponseCode = http.POST(jsonPayload);

        if (httpResponseCode > 0) {
            Serial.printf("[+] Upload successful (HTTP %d)\n", httpResponseCode);
            String response = http.getString();
            Serial.println(response);
        } else {
            Serial.printf("[!] Upload failed (HTTP %d)\n", httpResponseCode);
        }

        http.end();
        WiFi.disconnect();
    } else {
        Serial.println("\n[!] WiFi connection failed");
    }

    // Switch back to monitor mode
    switchToMonitorMode();
    sniffer->start();
    uploading = false;
}

String generateJSON() {
    JsonDocument doc;

    doc["badge_id"] = BADGE_ID;
    doc["firmware_version"] = FIRMWARE_VERSION;
    doc["timestamp"] = millis();
    doc["battery_voltage"] = batteryVoltage;

    JsonArray networks = doc["networks"].to<JsonArray>();

    int networkCount = sniffer->getNetworkCount();
    for (int i = 0; i < networkCount; i++) {
        WiFiNetwork* net = sniffer->getNetwork(i);
        if (net == nullptr) continue;

        JsonObject network = networks.add<JsonObject>();
        network["ssid"] = net->ssid;

        char bssidStr[18];
        snprintf(bssidStr, sizeof(bssidStr), "%02X:%02X:%02X:%02X:%02X:%02X",
                 net->bssid[0], net->bssid[1], net->bssid[2],
                 net->bssid[3], net->bssid[4], net->bssid[5]);
        network["bssid"] = bssidStr;

        network["channel"] = net->channel;
        network["rssi"] = net->rssi;

        const char* encTypes[] = {"Open", "WEP", "WPA", "WPA2", "WPA/WPA2", "WPA2-Ent", "WPA3"};
        network["encryption"] = encTypes[min(net->encryption, (uint8_t)6)];

        network["first_seen"] = net->first_seen;
        network["last_seen"] = net->last_seen;
        network["frame_count"] = net->frame_count;
    }

    String output;
    serializeJson(doc, output);
    return output;
}

void switchToStationMode() {
    esp_wifi_stop();
    esp_wifi_set_mode(WIFI_MODE_STA);
    esp_wifi_start();
}

void switchToMonitorMode() {
    WiFi.mode(WIFI_STA);
    esp_wifi_set_promiscuous(false);
    delay(100);
}
