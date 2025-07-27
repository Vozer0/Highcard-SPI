from simple import MQTTClient
import ssl
from time import sleep
from oled_display import display_text


class sslWrap:
    def __init__(self):
        self.wrap_socket = ssl.wrap_socket


def message_callback(topic, msg):
    """Handle incoming MQTT messages"""
    
    try:
        topic_str = topic.decode('utf-8')
        message = msg.decode('utf-8')
        
        print(f"=== MQTT MESSAGE RECEIVED ===")
        print(f"Topic: '{topic_str}'")
        print(f"Message: '{message}'")
        print(f"Message length: {len(message)}")
        
        # Display on OLED that we got a message
        display_text(f"Got: {message}")
        
        # Also check if it's the display topic
        if topic_str == "display":
            print("Processing display topic message")
            display_text(message)
        else:
            print(f"Topic '{topic_str}' doesn't match 'display'")
            # Show what topic we got
            display_text(f"Topic: {topic_str}")
        
        print("=== END MESSAGE PROCESSING ===")
        
    except Exception as e:
        print(f"Error in message callback: {e}")
        try:
            display_text(f"Callback Error: {str(e)[:10]}")
        except:
            print("Could not display error on OLED")


def connect_mqtt(mqtt_server, mqtt_user, mqtt_pass):
    try:
        print(f"Connecting to MQTT broker: {mqtt_server}")
        print(f"Using username: {mqtt_user}")
        
        client = MQTTClient(
            client_id=b"pico_device_001",  # More unique client ID
            server=mqtt_server,
            port=8883,
            user=mqtt_user.encode() if isinstance(mqtt_user, str) else mqtt_user,
            password=mqtt_pass.encode() if isinstance(mqtt_pass, str) else mqtt_pass,
            keepalive=3000, 
            ssl=sslWrap()     
        )
        
        # Set the callback function
        client.set_callback(message_callback)
        
        print("Attempting MQTT connection...")
        client.connect()
        print("Connected to MQTT successfully!")
        
        # Subscribe to the display topic
        client.subscribe(b"display")
        print("Subscribed to 'display' topic")
        
        return client
        
    except Exception as e:
        print(f"MQTT connection failed: {e}")
        print("Check your credentials and network connection")
        raise


import network

def connect_internet(ssid, password=None):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    found = False
    while not found:
        print("Scanning for networks...")
        nets = wlan.scan()
        for net in nets:
            net_ssid = net[0].decode()
            print(net_ssid)
            if net_ssid == ssid:
                found = True
                break
        if not found:
            print(f"SSID '{ssid}' not found, rescanning in 2s...")
            sleep(2)
    if not password:
        wlan.connect(ssid)
    else:
        wlan.connect(ssid, password)
    # Just wait for connection, don't scan again
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip


# Sensor data publishing functions for React integration
def publish_sensor_data(client, temp=None, humidity=None, light=None, distance=None):
    """
    Publish individual sensor readings to MQTT topics that the backend expects
    Backend subscribes to: 'temp', 'humidity', 'light', 'ultrasonic'
    """
    try:
        if temp is not None:
            client.publish(b"temp", str(temp).encode())
            print(f"Published temperature: {temp}")
            
        if humidity is not None:
            client.publish(b"humidity", str(humidity).encode())
            print(f"Published humidity: {humidity}")
            
        if light is not None:
            client.publish(b"light", str(light).encode())
            print(f"Published light: {light}")
            
        if distance is not None:
            client.publish(b"ultrasonic", str(distance).encode())
            print(f"Published distance: {distance}")
            
        return True
    except Exception as e:
        print(f"Error publishing sensor data: {e}")
        return False


def send_all_sensors(client, sensor_data):
    """
    Send all sensor data from the sensors.py get_all_sensor_data() function
    Expected format: {'temperature': 23, 'humidity': 60, 'light': 650, 'distance': 15.7}
    """
    try:
        print(f"DEBUG: Sending sensor data: {sensor_data}")  # Debug print
        result = publish_sensor_data(
            client,
            temp=sensor_data.get('temperature'),
            humidity=sensor_data.get('humidity'), 
            light=sensor_data.get('light'),
            distance=sensor_data.get('distance')
        )
        print(f"DEBUG: Publish result: {result}")  # Debug print
        return result
    except Exception as e:
        print(f"Error sending all sensors: {e}")
        return False

