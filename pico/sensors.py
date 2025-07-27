from machine import Pin, ADC
import time
import dht
from time import sleep_us


# Hardware setup - OLED uses working pins (8, 9), sensors use separate pins
trigger = Pin(21, Pin.OUT)
echo = Pin(20, Pin.IN)
sensor = dht.DHT11(Pin(28)) 
ldr = ADC(Pin(26))

# Note: OLED uses your working setup:
# Pin 8 → SDA, Pin 9 → SCL (I2C Bus 0 at 200kHz)
# Sensors are on separate pins and don't conflict


def get_light_reading():
    """
    Read light level from photoresistor (LDR)
    Returns: float - light level in lumens
    """
    try:
        raw = ldr.read_u16() 
        voltage = raw * 3.3 / 65535
        lumen_val = (0.344 * voltage) - 0.148
        return round(lumen_val, 2)
    except Exception as e:
        print(f"Light sensor error: {e}")
        return None


def get_temperature_humidity():
    """
    Read temperature and humidity from DHT11 sensor
    Returns: tuple (temperature_celsius, humidity_percent) or (None, None) on error
    """
    try:
        # DHT11 needs time between readings
        sleep_us(100000)  # 100ms delay
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print(f"DHT11 readings - Temp: {temp}°C, Humidity: {hum}%")
        return (temp, hum)
    except Exception as e:
        print(f"Temperature/Humidity sensor error: {e}")
        return (None, None)


def get_distance():
    """
    Read distance from ultrasonic sensor
    Returns: float - distance in centimeters
    """
    try:
        # Send ultrasonic pulse
        trigger.low()
        time.sleep_us(2)
        trigger.high()
        time.sleep_us(5)
        trigger.low()

        # Measure echo response time
        while echo.value() == 0:
            signal_off = time.ticks_us()
        while echo.value() == 1:
            signal_on = time.ticks_us()
        
        time_passed = signal_on - signal_off
        distance = (time_passed * 0.0343) / 2
        
        return round(distance, 1)
    except Exception as e:
        print(f"Ultrasonic sensor error: {e}")
        return None


def get_all_sensor_data():
    """
    Read all sensors and return formatted data for MQTT transmission
    Returns: dict with all sensor readings and timestamp
    """
    # Get all sensor readings
    light = get_light_reading()
    temp, humidity = get_temperature_humidity()
    distance = get_distance()
    
    # Create data package
    sensor_data = {
        "light": light,
        "temperature": temp,
        "humidity": humidity,
        "distance": distance,
        "timestamp": time.time()
    }
    
    return sensor_data


def print_sensor_data():
    """
    Debug function to print sensor readings to console
    Useful for testing without MQTT
    """
    data = get_all_sensor_data()
    print(f"=== Sensor Readings ===")
    print(f"Light: {data['light']} lumens")
    print(f"Temperature: {data['temperature']}°C")
    print(f"Humidity: {data['humidity']}%")
    print(f"Distance: {data['distance']} cm")
    print(f"Timestamp: {data['timestamp']}")
    print("=" * 23)


# Test function - only runs when file is executed directly
if __name__ == "__main__":
    try:
        print("Testing sensors (no display)...")
        while True:
            print_sensor_data()
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nSensor test stopped.")
