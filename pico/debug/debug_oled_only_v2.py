"""
Debug script to test OLED display only (no sensors)
Use this to verify OLED is working before adding sensors
"""

from connections import connect_mqtt, connect_internet
from oled_display import display_text, clear_display, oled, test_display
from time import sleep


def main_oled_test():
    try:
        print("=== OLED ONLY DEBUG TEST ===")
        
        # Test OLED hardware first
        print("Testing OLED display...")
        clear_display()
        display_text("OLED Test Started")
        sleep(2)
        
        # Run display test
        test_display()
        sleep(2)
        
        # Test WiFi connection with OLED feedback
        clear_display()
        display_text("Connecting WiFi...")
        sleep(1)
        
        connect_internet("SM-Vozer0", password="DVoce701204")
        
        display_text("WiFi Connected!")
        sleep(2)
        
        # Test MQTT connection
        display_text("Connecting MQTT...")
        sleep(1)
        
        try:
            client = connect_mqtt("09f1b50573094b6894b56ef79a8f1140.s1.eu.hivemq.cloud", "David2", "High_Card16")
            display_text("MQTT Connected!")
            sleep(2)
            
            # Test message receiving only
            display_text("Ready for messages")
            sleep(2)
            
            # Simple message loop without sensors
            while True:
                try:
                    client.check_msg()
                    sleep(1)
                    
                    # Just show we're alive
                    display_text("Listening...")
                    sleep(1)
                    
                except Exception as e:
                    print(f"Message loop error: {e}")
                    display_text("Loop Error")
                    sleep(2)
                    
        except Exception as mqtt_error:
            print(f"MQTT error: {mqtt_error}")
            display_text("MQTT Failed")
            sleep(3)
            
    except KeyboardInterrupt:
        print("Keyboard interrupt - exiting")
        clear_display()
        
    except Exception as e:
        print(f"Main error: {e}")
        try:
            display_text(f"Error: {str(e)[:15]}")
        except:
            print("Could not display error")


if __name__ == "__main__":
    main_oled_test()
