#ifndef WIFI_SNIFFER_H
#define WIFI_SNIFFER_H

#include <Arduino.h>
#include <esp_wifi.h>
#include <esp_wifi_types.h>

// WiFi Network Structure
struct WiFiNetwork {
    char ssid[33];
    uint8_t bssid[6];
    int8_t channel;
    int8_t rssi;
    uint8_t encryption;
    uint32_t first_seen;
    uint32_t last_seen;
    uint32_t frame_count;
    bool updated;  // Flag for visualization
};

// Encryption Types
#define WIFI_AUTH_OPEN 0
#define WIFI_AUTH_WEP 1
#define WIFI_AUTH_WPA_PSK 2
#define WIFI_AUTH_WPA2_PSK 3
#define WIFI_AUTH_WPA_WPA2_PSK 4
#define WIFI_AUTH_WPA2_ENTERPRISE 5
#define WIFI_AUTH_WPA3_PSK 6

class WiFiSniffer {
public:
    WiFiSniffer(int maxNetworks);
    ~WiFiSniffer();

    void begin();
    void start();
    void stop();
    void update();

    int getNetworkCount();
    WiFiNetwork* getNetwork(int index);
    WiFiNetwork* getAllNetworks();
    void clearNetworks();

    void setChannel(uint8_t channel);
    uint8_t getCurrentChannel();

    static void packetHandler(void* buf, wifi_promiscuous_pkt_type_t type);

private:
    WiFiNetwork* networks;
    int maxNetworks;
    int networkCount;
    uint8_t currentChannel;
    unsigned long lastChannelHop;
    bool scanning;

    int findNetwork(uint8_t* bssid);
    void addOrUpdateNetwork(uint8_t* bssid, const char* ssid, int8_t rssi,
                           uint8_t channel, uint8_t encryption);
    const char* getEncryptionString(uint8_t encryption);
};

// Global instance pointer for callback
extern WiFiSniffer* g_sniffer;

#endif // WIFI_SNIFFER_H
