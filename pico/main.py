from connections import connect_mqtt, connect_internet
from oled_display import display_text, clear_display, oled, test_display
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
                sleep(2)  # Check every 2 seconds
            except Exception as e:
                print(f"Error in message loop: {e}")
                display_text(f"MQTT Error: {str(e)[:15]}")
                sleep(5)  # Wait before retrying

    except KeyboardInterrupt:
        print('keyboard interrupt')
        clear_display()
        
        
if __name__ == "__main__":
    main()



