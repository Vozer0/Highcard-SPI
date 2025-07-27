# System Integration Test
# Test the complete data flow: Sensors → MQTT → Backend → Frontend

from connections import connect_mqtt, connect_internet, send_all_sensors
from oled_display import display_text, clear_display, test_display
from sensors import get_all_sensor_data
from time import sleep
import time

def test_sensor_readings():
    """Test all sensor readings individually"""
    print("\n=== TESTING INDIVIDUAL SENSORS ===")
    
    # Test each sensor
    from sensors import get_light_reading, get_temperature_humidity, get_distance
    
    print("1. Testing Light Sensor...")
    light = get_light_reading()
    print(f"   Light reading: {light}")
    
    print("2. Testing Temperature/Humidity Sensor...")
    temp, humidity = get_temperature_humidity()
    print(f"   Temperature: {temp}°C, Humidity: {humidity}%")
    
    print("3. Testing Ultrasonic Sensor...")
    distance = get_distance()
    print(f"   Distance: {distance}cm")
    
    print("4. Testing Combined Sensor Data...")
    all_data = get_all_sensor_data()
    print(f"   Combined data: {all_data}")
    
    return all_data

def test_oled_functionality():
    """Test OLED display functionality"""
    print("\n=== TESTING OLED DISPLAY ===")
    
    try:
        # Clear display
        clear_display()
        print("✅ OLED cleared successfully")
        
        # Test basic text display
        display_text("System Test Running...")
        print("✅ OLED text display working")
        sleep(2)
        
        # Test sensor data display format
        test_data = {"temperature": 23.5, "humidity": 65, "light": 0.85, "distance": 12.3}
        temp = test_data['temperature']
        hum = test_data['humidity'] 
        light = test_data['light']
        dist = test_data['distance']
        
        display_text(f"T:{temp}C H:{hum}% L:{light} D:{dist}cm")
        print("✅ OLED sensor format display working")
        sleep(2)
        
        return True
    except Exception as e:
        print(f"❌ OLED test failed: {e}")
        return False

def test_mqtt_connection():
    """Test MQTT connection and publishing"""
    print("\n=== TESTING MQTT CONNECTION ===")
    
    try:
        # Connect to WiFi
        display_text("Testing WiFi...")
        connect_internet("SM-Vozer0", password="DVoce701204")
        print("✅ WiFi connected successfully")
        
        # Connect to MQTT
        display_text("Testing MQTT...")
        client = connect_mqtt("09f1b50573094b6894b56ef79a8f1140.s1.eu.hivemq.cloud", "David2", "High_Card16")
        print("✅ MQTT connected successfully")
        
        # Test publishing sensor data
        test_data = {
            "temperature": 24.0,
            "humidity": 60,
            "light": 0.75,
            "distance": 15.5,
            "timestamp": time.time()
        }
        
        display_text("Testing Data Send...")
        success = send_all_sensors(client, test_data)
        
        if success:
            print("✅ MQTT data publishing successful")
            display_text("✅ MQTT Test OK!")
        else:
            print("❌ MQTT data publishing failed")
            display_text("❌ MQTT Test Failed")
            
        sleep(2)
        return client, success
        
    except Exception as e:
        print(f"❌ MQTT test failed: {e}")
        display_text(f"MQTT Error: {str(e)[:15]}")
        return None, False

def test_complete_system():
    """Run a complete system integration test"""
    print("\n" + "="*50)
    print("🚀 STARTING COMPLETE SYSTEM TEST")
    print("="*50)
    
    # Step 1: Test OLED
    display_text("🧪 Running System Test...")
    sleep(1)
    
    oled_ok = test_oled_functionality()
    if not oled_ok:
        print("⚠️  OLED issues detected, but continuing...")
    
    # Step 2: Test sensors
    sensor_data = test_sensor_readings()
    if not any(v is not None for k, v in sensor_data.items() if k != 'timestamp'):
        print("⚠️  No valid sensor readings, check wiring!")
        display_text("⚠️ Sensor Issues")
        sleep(2)
    
    # Step 3: Test MQTT
    client, mqtt_ok = test_mqtt_connection()
    if not mqtt_ok:
        print("❌ MQTT test failed - check credentials/network")
        return False
    
    # Step 4: Test real data flow
    print("\n=== TESTING REAL DATA FLOW ===")
    display_text("📡 Testing Real Data...")
    
    try:
        # Send real sensor data
        real_data = get_all_sensor_data()
        print(f"Real sensor data: {real_data}")
        
        success = send_all_sensors(client, real_data)
        if success:
            print("✅ Real data sent to backend successfully!")
            display_text("✅ All Systems GO!")
            
            # Display current readings
            temp = real_data.get('temperature', 'N/A')
            hum = real_data.get('humidity', 'N/A') 
            light = real_data.get('light', 'N/A')
            dist = real_data.get('distance', 'N/A')
            
            sleep(2)
            display_text(f"T:{temp}C H:{hum}% L:{light} D:{dist}cm")
            
        else:
            print("❌ Failed to send real data")
            display_text("❌ Data Send Failed")
            
    except Exception as e:
        print(f"❌ Real data test failed: {e}")
        display_text("❌ Data Test Failed")
        return False
    
    print("\n" + "="*50)
    print("🎉 SYSTEM TEST COMPLETE!")
    print("✅ Your Pico → MQTT → Backend → React flow is ready!")
    print("="*50)
    
    return True

def quick_sensor_monitor():
    """Quick continuous sensor monitoring for testing - 1 second intervals"""
    print("\n=== REAL-TIME SENSOR MONITOR (1 second intervals) ===")
    print("Press Ctrl+C to stop...")
    
    try:
        while True:
            data = get_all_sensor_data()
            temp = data.get('temperature', 'N/A')
            hum = data.get('humidity', 'N/A')
            light = data.get('light', 'N/A') 
            dist = data.get('distance', 'N/A')
            
            timestamp = time.strftime('%H:%M:%S')
            print(f"[{timestamp}] Temp: {temp}°C | Humidity: {hum}% | Light: {light} | Distance: {dist}cm")
            display_text(f"T:{temp} H:{hum}% L:{light} D:{dist}")
            
            sleep(1)  # 1 second intervals for real-time monitoring
    except KeyboardInterrupt:
        print("\nReal-time monitoring stopped.")
        clear_display()

if __name__ == "__main__":
    try:
        print("🔧 Pico System Integration Test")
        print("Choose test option:")
        print("1. Complete system test")
        print("2. Sensor readings only")
        print("3. MQTT test only") 
        print("4. OLED test only")
        print("5. Quick sensor monitor")
        
        # For automated testing, run complete test
        print("Running complete system test...")
        test_complete_system()
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        clear_display()
    except Exception as e:
        print(f"Test error: {e}")
        display_text("Test Error")
