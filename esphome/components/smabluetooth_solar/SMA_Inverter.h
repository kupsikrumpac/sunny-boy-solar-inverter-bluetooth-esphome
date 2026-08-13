#pragma once
#ifndef ESP32_SMA_INVERTER_H
#define ESP32_SMA_INVERTER_H

// FreeRTOS
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/stream_buffer.h"
#include "freertos/event_groups.h"

// ESP-IDF Bluetooth (Classic / Bluedroid / SPP)
#include "esp_bt.h"
#include "esp_bt_main.h"
#include "esp_gap_bt_api.h"
#include "esp_spp_api.h"

#include <string>
#include <cstring>
#include <cstdint>
#include <ctime>
#include <cmath>

#define DEBUG_SMA 0

namespace esphome {
namespace smabluetooth_solar {

#define tokWh(value64)    (double)(value64)/1000.0
#define tokW(value32)     (float)(value32)/1000.0
#define toW(value32)      (float)(value32)/1.0
#define toHour(value64)   (double)(value64)/3600
#define toAmp(value32)    (float)(value32)/1000
#define toVolt(value32)   (float)(value32)/100
#define toHz(value32)     (float)(value32)/100
#define toPercent(value32)(float)(value32)/100
#define toTemp(value32)   (float)(value32)/100

#define UG_USER      0x07
#define UG_INSTALLER 0x0A

#define ARCH_DAY_SIZE 288
#define COMMBUFSIZE 2048
#define MAX_PCKT_BUF_SIZE COMMBUFSIZE

#define BTH_L2SIGNATURE 0x656003FF
#define USERGROUP UG_USER

#define NaN_S16 0x8000
#define NaN_U16 0xFFFF
#define NaN_S32 (int32_t) 0x80000000
#define NaN_U32 (uint32_t)0xFFFFFFFF
#define NaN_S64 (int64_t) 0x8000000000000000
#define NaN_U64 (uint64_t)0xFFFFFFFFFFFFFFFF

inline const bool is_NaN(const int16_t S16)  { return S16 == NaN_S16; }
inline const bool is_NaN(const uint16_t U16) { return U16 == NaN_U16; }
inline const bool is_NaN(const int32_t S32)  { return S32 == NaN_S32; }
inline const bool is_NaN(const uint32_t U32) { return U32 == NaN_U32; }
inline const bool is_NaN(const int64_t S64)  { return S64 == NaN_S64; }
inline const bool is_NaN(const uint64_t U64) { return U64 == NaN_U64; }

// ---- Event group bits for BT state signalling between task and callbacks ----
#define BT_EVT_SPP_INIT     (BIT0)
#define BT_EVT_DISC_DONE    (BIT1)
#define BT_EVT_CONNECTED    (BIT2)
#define BT_EVT_DISCONNECTED (BIT3)

enum SMA_DATATYPE {
    DT_ULONG  = 0,
    DT_STATUS = 8,
    DT_STRING = 16,
    DT_FLOAT  = 32,
    DT_SLONG  = 64
};

enum E_RC {
    E_OK =          0,
    E_INIT =       -1,
    E_INVPASSW =   -2,
    E_RETRY =      -3,
    E_EOF =        -4,
    E_NODATA =     -5,
    E_OVERFLOW =   -6,
    E_BADARG =     -7,
    E_CHKSUM =     -8,
    E_INVRESP =    -9,
    E_ARCHNODATA = -10,
};

struct InverterData {
    uint8_t btAddress[6];
    uint8_t SUSyID;
    uint32_t Serial;
    uint8_t NetID;
    int32_t Pmax;
    int32_t TotalPac;
    int32_t Pac;
    int32_t Pac1;
    int32_t Pac2;
    int32_t Pac3;
    int32_t Uac1;
    int32_t Uac2;
    int32_t Uac3;
    int32_t Iac1;
    int32_t Iac2;
    int32_t Iac3;
    int32_t Pdc1;
    int32_t Pdc2;
    int32_t Udc1;
    int32_t Udc2;
    int32_t Idc1;
    int32_t Idc2;
    int32_t GridFreq;
    int32_t Eta;
    int32_t InvTemp;
    uint64_t EToday;
    uint64_t ETotal;
    uint64_t dayWh[ARCH_DAY_SIZE];
    time_t  DayStartTime;
    bool hasDayData;
    bool hasMonthData;
    time_t   LastTime;
    uint64_t OperationTime;
    uint64_t FeedInTime;
    int32_t DevStatus;
    int32_t GridRelay;
    E_RC     status;
    uint32_t MeteringGridMsTotWOut;
    uint32_t MeteringGridMsTotWIn;
    time_t WakeupTime;
    std::string DeviceName;
    std::string SWVersion;
    uint32_t DeviceType;
    uint32_t DeviceClass;
    std::string InverterTimestamp;
};

struct DisplayData {
    float BTSigStrength;
    float Pmax;
    float TotalPac;
    float Pac;
    float Pac1;
    float Pac2;
    float Pac3;
    float Uac1;
    float Uac2;
    float Uac3;
    float Iac1;
    float Iac2;
    float Iac3;
    float InvTemp;
    float Pdc1;
    float Pdc2;
    float Udc1;
    float Udc2;
    float Idc1;
    float Idc2;
    float GridFreq;
    float EToday;
    float ETotal;
    bool needsMissingValues = false;
};

enum getInverterDataType {
    EnergyProduction    = 1 << 0,
    SpotDCPower         = 1 << 1,
    SpotDCVoltage       = 1 << 2,
    SpotACPower         = 1 << 3,
    SpotACVoltage       = 1 << 4,
    SpotGridFrequency   = 1 << 5,
    SpotACTotalPower    = 1 << 8,
    TypeLabel           = 1 << 9,
    OperationTime       = 1 << 10,
    SoftwareVersion     = 1 << 11,
    DeviceStatus        = 1 << 12,
    GridRelayStatus     = 1 << 13,
    BatteryChargeStatus = 1 << 14,
    BatteryInfo         = 1 << 15,
    InverterTemp        = 1 << 16,
    MeteringGridMsTotW  = 1 << 17,
    sbftest             = 1 << 31
};

#pragma pack(push, 1)
typedef struct __attribute__((packed)) PacketHeader {
    uint8_t        SOP;
    unsigned short pkLength;
    uint8_t        pkChecksum;
    uint8_t        SourceAddr[6];
    uint8_t        DestinationAddr[6];
    unsigned short command;
} L1Hdr;
#pragma pack(pop)

class ESP32_SMA_Inverter {
  public:
    // Konstruktor přizpůsobený pro volání ze smabluetooth_solar.cpp
    ESP32_SMA_Inverter(std::string mac = "", std::string pw = "") {
        if (!mac.empty() || !pw.empty()) {
            setup(mac, pw, 500);
        }
    }

    ~ESP32_SMA_Inverter() {}

    static ESP32_SMA_Inverter* getInstance() {
        static ESP32_SMA_Inverter instance;
        return &instance;
    }

    // Nastavení parametrů
    void setup(std::string mac, std::string pw, uint32_t delay_values_ms) {
        // Konverze MAC
        int values[6];
        if (sscanf(mac.c_str(), "%x:%x:%x:%x:%x:%x", 
                   &values[0], &values[1], &values[2], 
                   &values[3], &values[4], &values[5]) == 6) {
            for (int i = 0; i < 6; ++i) {
                smaBTAddress[i] = (uint8_t) values[i];
            }
        }
        strncpy(smaInvPass, pw.c_str(), sizeof(smaInvPass) - 1);
        delay_values_ms_ = delay_values_ms;
    }

    // Spuštění bez parametrů (jak volá cpp)
    bool begin(const char *localName = "ESP32_SMA") {
        startBtTask();
        return true;
    }

    void startBtTask();
    void stopBtTask();

    // Metody požadované smabluetooth_solar.cpp
    uint16_t get_status() const {
        if (!btConnected_) return 0x08; // Odpojeno
        if (task_error_) return 0x04;   // Chyba
        return 0x00;                    // OK
    }

    float get_today_production() const { return dispData.EToday; }
    float get_total_energy_production() const { return dispData.ETotal; }
    float get_grid_frequency() const { return dispData.GridFreq; }

    float get_pv_voltage(size_t index) const {
        return (index == 0) ? dispData.Udc1 : dispData.Udc2;
    }
    float get_pv_current(size_t index) const {
        return (index == 0) ? dispData.Idc1 : dispData.Idc2;
    }
    float get_phase_voltage(size_t index) const {
        if (index == 0) return dispData.Uac1;
        if (index == 1) return dispData.Uac2;
        return dispData.Uac3;
    }
    float get_phase_current(size_t index) const {
        if (index == 0) return dispData.Iac1;
        if (index == 1) return dispData.Iac2;
        return dispData.Iac3;
    }
    float get_phase_active_power(size_t index) const {
        if (index == 0) return dispData.Pac1;
        if (index == 1) return dispData.Pac2;
        return dispData.Pac3;
    }
    bool get_grid_relay_status() const { return invData.GridRelay == 1; }
    float get_module_temp() const { return dispData.InvTemp; }

    std::string get_serial_number() const { return std::to_string(invData.Serial); }
    std::string get_software_version() const { return invData.SWVersion; }
    std::string get_device_type() const { return std::to_string(invData.DeviceType); }

    // Původní veřejné stavové funkce
    bool isDataReady()   const { return data_ready_; }
    void clearDataReady()      { data_ready_ = false; }
    bool hasTaskError()  const { return task_error_; }
    void clearTaskError()      { task_error_ = false; }
    bool isBtConnected() const { return btConnected_; }
    bool isNightModeActive() const { return night_mode_active_; }

    // Sdílená data
    InverterData invData  = InverterData();
    DisplayData  dispData = DisplayData();

  private:
    static void spp_callback(esp_spp_cb_event_t event, esp_spp_cb_param_t *param);
    static void gap_callback(esp_bt_gap_cb_event_t event, esp_bt_gap_cb_param_t *param);
    static void btTask(void *pvParameters);

    bool        isValidSender(const uint8_t expAddr[6], const uint8_t isAddr[6]);
    E_RC        getPacket(const uint8_t expAddr[6], int wait4Command);
    E_RC        getInverterDataCfl(uint32_t command, uint32_t first, uint32_t last);
    E_RC        getInverterData(enum getInverterDataType type);
    bool        getBT_SignalStrength();
    E_RC        initialiseSMAConnection();
    E_RC        logonSMAInverter();
    E_RC        logonSMAInverter(const char *password, const uint8_t user);
    void        logoffSMAInverter();

    uint8_t BTgetByte();
    void    BTsendPacket(uint8_t *btbuffer);
    void    flushRxBuffer();

    void writePacketHeader(uint8_t *buf, const uint16_t control, const uint8_t *destaddress);
    void writePacket(uint8_t *buf, uint8_t longwords, uint8_t ctrl, uint16_t ctrl2,
                     uint16_t dstSUSyID, uint32_t dstSerial);
    void writePacketTrailer(uint8_t *btbuffer);
    void writePacketLength(uint8_t *buf);
    void writeByte(uint8_t *btbuffer, uint8_t v);
    void write32(uint8_t *btbuffer, uint32_t v);
    void write16(uint8_t *btbuffer, uint16_t v);
    void writeArray(uint8_t *btbuffer, const uint8_t bytes[], int loopcount);

    // FreeRTOS & BT
    StreamBufferHandle_t rx_stream_buf_  = nullptr;
    EventGroupHandle_t   bt_event_group_ = nullptr;
    volatile TaskHandle_t bt_task_handle_ = nullptr;

    volatile uint32_t spp_handle_    = 0;
    uint8_t           discovered_scn_ = 1;

    volatile bool btConnected_        = false;
    volatile bool data_ready_         = false;
    volatile bool task_error_         = false;
    volatile bool stop_task_          = false;
    volatile bool sync_time_requested_  = false;
    volatile bool fetch_time_requested_ = false;
    bool night_mode_active_             = false;

    uint8_t  smaBTAddress[6] = {0};
    char     smaInvPass[12] = {0};
    uint32_t delay_values_ms_   = 500;

    uint8_t  btrdBuf[COMMBUFSIZE];
    uint8_t  pcktBuf[MAX_PCKT_BUF_SIZE];
    uint16_t pcktBufPos = 0;
    uint16_t pcktBufMax = 0;
    uint8_t  espBTAddress[6];

    uint16_t pcktID       = 1;
    bool     readTimeout  = false;
    uint16_t fcsChecksum  = 0xffff;

    uint32_t btgetByteTimeout = 5000;
};

} // namespace smabluetooth_solar
} // namespace esphome

#endif // ESP32_SMA_INVERTER_H
