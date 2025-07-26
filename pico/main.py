from connections import connect_mqtt, connect_internet
from oled_display import display_text, clear_display
from time import sleep


def main():
    try:
        # Initialize OLED display
        clear_display()
        display_text("Connecting...")
        connect_internet("SM-Vozero", password="DVoce701204") #ssid (wifi name), pass
        
        # HiveMQ Cloud connection - Cluster 2
        client = connect_mqtt("ae560d05cdca43359485c6741741a1e8.s1.eu.hivemq.cloud", "David2", "High_Card16")
        
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



