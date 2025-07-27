"""
Improved main.py with better error handling and component isolation
This version initializes components safely and handles failures gracefully
"""

from connections import connect_mqtt, connect_internet, send_all_sensors
from oled_display import display_text, clear_display, oled, test_display
from sensors import get_all_sensor_data
from time import sleep


def safe_display(message):
    """Safely display message with error handling"""
    try:
        display_text(message)
        print(f"OLED: {message}")
    except Exception as e:
        print(f"OLED Error: {e}, Message was: {message}")


def safe_clear():
    """Safely clear display with error handling"""
    try:
        clear_display()
    except Exception as e:
        print(f"OLED Clear Error: {e}")


def test_components():
    """Test each component before main loop"""
    print("=== COMPONENT TESTING ===")
    
    # 1. Test OLED first
    print("1. Testing OLED...")
    try:
        safe_clear()
        safe_display("Component Test")
        sleep(1)
        test_display()
        sleep(1)
        safe_display("OLED: OK")
        print("✅ OLED working")
        sleep(2)
    except Exception as e:
        print(f"❌ OLED failed: {e}")
        return False
    
    # 2. Test sensors separately
    print("2. Testing sensors...")
    try:
        safe_display("Testing sensors...")
        sensor_data = get_all_sensor_data()
        print(f"Sensor data: {sensor_data}")
        
        # Check if we got any valid data
        valid_readings = sum(1 for v in sensor_data.values() 
                           if v is not None and v != sensor_data.get('timestamp'))
        
        if valid_readings > 0:
            safe_display(f"Sensors: {valid_readings}/4 OK")
            print(f"✅ Sensors partially working ({valid_readings}/4)")
        else:
            safe_display("Sensors: Failed")
            print("⚠️  No sensor readings")
        
        sleep(2)
    except Exception as e:
        print(f"❌ Sensor test failed: {e}")
        safe_display("Sensors: Error")
        sleep(2)
    
    return True


def main():
    try:
        print("=== IMPROVED HIGH CARD MAIN ===")
        
        # Component testing phase
        if not test_components():
            print("Component testing failed - check OLED wiring")
            return
        
        # Network connection phase
        safe_clear()
        safe_display("Connecting WiFi...")
        sleep(1)
        
        try:
            connect_internet("SM-Vozer0", password="DVoce701204")
            safe_display("WiFi: Connected!")
            sleep(1)
        except Exception as e:
            print(f"WiFi failed: {e}")
            safe_display("WiFi: Failed")
            sleep(3)
            return
        
        # MQTT connection phase
        safe_display("Connecting MQTT...")
        sleep(1)
        
        try:
            client = connect_mqtt("09f1b50573094b6894b56ef79a8f1140.s1.eu.hivemq.cloud", "David2", "High_Card16")
            safe_display("MQTT: Connected!")
            sleep(2)
        except Exception as e:
            print(f"MQTT failed: {e}")
            safe_display("MQTT: Failed")
            sleep(3)
            return

        # Main operation phase
        safe_display("System Ready!")
        sleep(2)
        safe_clear()
        
        sensor_counter = 0
        
        while True:
            try:
                # Check for messages
                client.check_msg()
                
                # Sensor reading cycle
                sensor_counter += 1
                if sensor_counter >= 5:  # Every 10 seconds
                    print("=== SENSOR READING CYCLE ===")
                    
                    try:
                        # Clear display and show we're reading
                        safe_clear()
                        safe_display("Reading...")
                        sleep(0.5)
                        
                        # Get sensor data
                        sensor_data = get_all_sensor_data()
                        print(f"Raw sensor data: {sensor_data}")
                        
                        # Prepare display data with None handling
                        temp = sensor_data.get('temperature', 'N/A')
                        hum = sensor_data.get('humidity', 'N/A')
                        light = sensor_data.get('light', 'N/A')
                        dist = sensor_data.get('distance', 'N/A')
                        
                        # Format for display (shorter)
                        if temp is None: temp = "N/A"
                        if hum is None: hum = "N/A"
                        if light is None: light = "N/A"
                        if dist is None: dist = "N/A"
                        
                        display_line = f"T:{temp} H:{hum}% L:{light} D:{dist}"
                        safe_display(display_line)
                        
                        # Send to MQTT
                        try:
                            success = send_all_sensors(client, sensor_data)
                            if success:
                                print("✅ Data sent to React")
                            else:
                                print("❌ MQTT send failed")
                                
                        except Exception as mqtt_error:
                            print(f"MQTT send error: {mqtt_error}")
                        
                    except Exception as sensor_error:
                        print(f"Sensor cycle error: {sensor_error}")
                        safe_display("Sensor Error")
                    
                    sensor_counter = 0
                
                sleep(2)  # Main loop delay
                
            except Exception as loop_error:
                print(f"Main loop error: {loop_error}")
                safe_display("Loop Error")
                sleep(5)

    except KeyboardInterrupt:
        print('Keyboard interrupt - shutting down')
        safe_clear()
        
    except Exception as main_error:
        print(f"Main error: {main_error}")
        try:
            safe_display(f"Error: {str(main_error)[:10]}")
        except:
            pass


if __name__ == "__main__":
    main()
