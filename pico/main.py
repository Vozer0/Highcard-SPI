from connections import connect_mqtt, connect_internet
from oled_display import display_text, clear_display, oled
from time import sleep


def main():
    try:
        # Test OLED hardware
        print("Testing OLED...")
        oled.fill(1)  # Fill with white
        oled.show()
        sleep(2)
        oled.fill(0)  # Clear
        oled.text("OLED Test", 0, 0)
        oled.show()
        sleep(2)
        # Initialize OLED display
        clear_display()
        display_text("Connecting...")
        connect_internet("SM-Vozero", password="DVoce701204") #ssid (wifi name), pass
        
        # HiveMQ Cloud connection - Cluster 2
        client = connect_mqtt("09f1b50573094b6894b56ef79a8f1140.s1.eu.hivemq.cloud", "David2", "High_Card16")
        
        # Display connection success
        display_text("Connected!")
        sleep(2)
        clear_display()

        while True:
            client.check_msg()
            sleep(0.1)

    except KeyboardInterrupt:
        print('keyboard interrupt')
        clear_display()
        
        
if __name__ == "__main__":
    main()



