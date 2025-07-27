from machine import Pin, I2C
import network
from simple import MQTTClient
import ssl
from time import sleep
import ssd1306

# Quick MQTT test
def quick_mqtt_test():
    print("=== QUICK MQTT TEST ===")
    
    # Setup OLED for feedback
    i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=200000)  # Back to working configuration
    oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
    
    def show_message(msg):
        oled.fill(0)
        oled.text(msg, 0, 0, 1)
        oled.show()
        print(msg)
    
    show_message("MQTT Test Starting")
    sleep(2)
    
    # Connect to WiFi (assuming already connected)
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        show_message("WiFi not connected!")
        return
    
    show_message("WiFi OK, connecting MQTT")
    sleep(2)
    
    # SSL wrapper
    class sslWrap:
        def __init__(self):
            self.wrap_socket = ssl.wrap_socket
    
    # Message handler
    def test_callback(topic, msg):
        topic_str = topic.decode('utf-8')
        message = msg.decode('utf-8')
        print(f"🎉 RECEIVED: Topic='{topic_str}', Message='{message}'")
        show_message(f"Got: {message}")
    
    try:
        # Create MQTT client
        client = MQTTClient(
            client_id=b"pico_test_123",
            server="09f1b50573094b6894b56ef79a8f1140.s1.eu.hivemq.cloud",
            port=8883,
            user="David2",
            password="High_Card16",
            keepalive=3000,
            ssl=sslWrap()
        )
        
        client.set_callback(test_callback)
        
        print("Connecting to MQTT...")
        client.connect()
        print("Connected!")
        
        show_message("MQTT Connected!")
        sleep(2)
        
        # Subscribe to display topic
        client.subscribe(b"display")
        print("Subscribed to 'display' topic")
        
        show_message("Waiting for messages...")
        
        # Listen for messages
        for i in range(60):  # Listen for 60 seconds
            print(f"Checking messages... {i+1}/60")
            client.check_msg()
            sleep(1)
            
            # Show we're listening
            if i % 10 == 0:
                show_message(f"Listening... {i+1}/60")
        
        show_message("Test complete")
        
    except Exception as e:
        error_msg = f"Error: {str(e)[:20]}"
        print(f"MQTT Test Error: {e}")
        show_message(error_msg)

if __name__ == "__main__":
    quick_mqtt_test()
