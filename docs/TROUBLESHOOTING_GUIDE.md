# Comprehensive Debug and Test Guide for Current System

## 🔧 **Updated Debug Strategy for Your Improved Code**

### **Quick Problem Diagnosis:**

#### **🚨 If Nothing Works:**
1. **Run**: `debug/debug_oled_only_v2.py` - Tests OLED + WiFi only
2. **Check**: OLED displays "OLED Test Started"
3. **If fails**: Hardware connection issue (pins 8/9, power, ground)

#### **🌐 If WiFi Fails:**
1. **Check**: SSID "SM-Vozer0" and password "DVoce701204" 
2. **Run**: `debug/mqtt_test_v2.py` - Tests MQTT connection only
3. **Look for**: "Connected to HiveMQ" message

#### **📊 If Sensors Don't Work:**
1. **Run**: `debug/debug_sensors_only_v2.py` - Tests sensors without OLED/WiFi
2. **Check each sensor individually**:
   - Light (Pin 26) - Should change with light level
   - DHT11 (Pin 28) - Needs 4.7kΩ pull-up resistor
   - Ultrasonic (Pins 20/21) - Check trigger/echo connections

#### **🔄 If MQTT Data Not Reaching React:**
1. **Run**: `tests/system_test_v2.py` - Full system integration test
2. **Check backend console** for MQTT message reception
3. **Verify React WebSocket** connection to backend

### **🧪 Test Files Aligned with Current Code:**

#### **Hardware Tests:**
- `tests/sensor_quality_test_v2.py` - Validates sensor accuracy
- `tests/distance_speed_test.py` - Tests ultrasonic performance  
- `tests/i2c_frequency_test.py` - OLED I2C timing tests

#### **Integration Tests:**
- `tests/system_test_v2.py` - Complete Pico → MQTT → Backend → React flow
- `tests/triple_check_verification_v2.py` - Multi-stage system verification

#### **Debug Tools:**
- `debug/debug_oled_only_v2.py` - OLED + WiFi isolation test
- `debug/debug_sensors_only_v2.py` - Sensor-only testing
- `debug/mqtt_test_v2.py` - MQTT connection testing
- `debug/pin_test.py` - GPIO pin functionality
- `debug/oled_targeted_debug.py` - Specific OLED issues

### **📋 Diagnostic Checklist for Current System:**

#### **Power & Connections:**
- [ ] Pico powered via USB (VBUS = 5V)
- [ ] All grounds connected
- [ ] OLED: Pin 8 (SDA), Pin 9 (SCL)
- [ ] DHT11: Pin 28 + pull-up resistor
- [ ] Ultrasonic: Pin 21 (trigger), Pin 20 (echo)
- [ ] LDR: Pin 26 (ADC) + voltage divider

#### **Software Stack:**
- [ ] `main.py` imports: connections, oled_display, sensors
- [ ] WiFi connects to "SM-Vozer0"
- [ ] MQTT connects to HiveMQ Cloud
- [ ] Backend running on port 8000
- [ ] React frontend connecting to backend

#### **Data Flow Verification:**
- [ ] Sensors reading every 1 second
- [ ] MQTT publishing to: temp, humidity, light, ultrasonic
- [ ] Backend receiving and forwarding via WebSocket
- [ ] React displaying real-time updates
- [ ] OLED showing current sensor values

### **🛠️ Troubleshooting Commands:**

#### **Step 1 - Hardware Test:**
```python
# Run this first
exec(open('debug/debug_oled_only_v2.py').read())
```

#### **Step 2 - Sensor Test:**  
```python
# If OLED works, test sensors
exec(open('debug/debug_sensors_only_v2.py').read())
```

#### **Step 3 - Integration Test:**
```python
# If sensors work, test full system
exec(open('tests/system_test_v2.py').read())
```

### **🔍 Error Pattern Recognition:**

#### **"OLED Working!" doesn't appear:**
- Check I2C pins (8/9)
- Verify 200kHz frequency
- Check power connections

#### **WiFi connects but MQTT fails:**
- Check HiveMQ credentials
- Verify internet connection
- Test with `debug/mqtt_test_v2.py`

#### **Sensors return None:**
- Check individual sensor connections
- Run `tests/sensor_quality_test_v2.py`
- Verify voltage levels

#### **React shows "Loading...":**
- Check backend console for MQTT messages
- Verify WebSocket connection
- Test with `tests/system_test_v2.py`

### **📊 Performance Monitoring:**

#### **Expected Performance:**
- Sensor readings: Every 1 second
- MQTT latency: < 100ms
- React updates: Real-time
- Memory usage: < 50KB on Pico

#### **Monitoring Tools:**
- `tests/distance_speed_test.py` - Performance benchmarks
- `tests/sensor_calibration.py` - Accuracy validation
- Backend console logs - Data flow monitoring

This guide is specifically updated for your current improved code structure and will help diagnose issues with your exact setup!
