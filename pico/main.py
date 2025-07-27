from connections import connect_mqtt, connect_internet, send_all_sensors
from oled_display import display_text, clear_display, oled, test_display
from sensors import get_all_sensor_data
from time import sleep


def main():
    try:
        # Test OLED hardware with working I2C frequency
        print("Testing OLED with correct I2C frequency...")
        
        # Simple test first
        clear_display()
        display_text("OLED Working!")
        sleep(2)
        
        # Run comprehensive display test
        test_display()
        sleep(2)
        
        # Clear and show connection message
        clear_display()
        display_text("Connecting WiFi...")
        sleep(1)
        
        connect_internet("SM-Vozer0", password="DVoce701204") #ssid (wifi name), pass
        
        # Show WiFi connected
        display_text("WiFi OK! Connecting MQTT...")
        sleep(1)
        
        # HiveMQ Cloud connection - Cluster 2
        try:
            client = connect_mqtt("09f1b50573094b6894b56ef79a8f1140.s1.eu.hivemq.cloud", "David2", "High_Card16")
            
            # Display connection success
            display_text("All Connected! Ready to go!")
            sleep(3)
            clear_display()
            
        except Exception as e:
            print(f"MQTT connection error: {e}")
            display_text("MQTT Failed! Check credentials")
            sleep(3)
            return  # Exit if MQTT fails

        while True:
            try:
                print("Checking for MQTT messages...")
                client.check_msg()
                
                # Read and send sensor data EVERY SECOND for real-time monitoring
                print("Reading sensors...")
                try:
                    sensor_data = get_all_sensor_data()
                    print(f"Sensor data: {sensor_data}")  # Debug print
                    
                    # Check if we got valid sensor data
                    if any(v is not None for v in sensor_data.values() if v != sensor_data.get('timestamp')):
                        # Display current sensor readings on OLED
                        temp = sensor_data['temperature'] if sensor_data['temperature'] is not None else "N/A"
                        hum = sensor_data['humidity'] if sensor_data['humidity'] is not None else "N/A"
                        light = sensor_data['light'] if sensor_data['light'] is not None else "N/A"
                        dist = sensor_data['distance'] if sensor_data['distance'] is not None else "N/A"
                        
                        display_text(f"T:{temp}C H:{hum}% L:{light} D:{dist}cm")
                        
                        # Send to React via MQTT - EVERY SECOND for real-time updates
                        success = send_all_sensors(client, sensor_data)
                        if success:
                            print("✅ Sensor data sent to React!")
                        else:
                            print("❌ Failed to send sensor data")
                            
                    else:
                        print("⚠️  No valid sensor data received")
                        display_text("Sensor Error")
                        
                except Exception as sensor_error:
                    print(f"Sensor error: {sensor_error}")
                    display_text("Sensor Error - Check wiring")
                
                sleep(1)  # Read sensors every 1 second for real-time monitoring
            except Exception as e:
                print(f"Error in message loop: {e}")
                display_text(f"MQTT Error: {str(e)[:15]}")
                sleep(5)  # Wait before retrying

    except KeyboardInterrupt:
        print('keyboard interrupt')
        clear_display()
        
        
if __name__ == "__main__":
    main()



