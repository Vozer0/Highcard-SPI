"""
Debug script to test sensors only (no OLED, no WiFi)
Use this to verify sensors work in isolation
"""

from sensors import get_all_sensor_data, get_light_reading, get_temperature_humidity, get_distance
from time import sleep


def test_sensors_individually():
    """Test each sensor separately"""
    print("=== INDIVIDUAL SENSOR TESTS ===")
    
    # Test light sensor
    print("\n1. Testing Light Sensor (LDR on pin 26)...")
    try:
        light = get_light_reading()
        print(f"   Light reading: {light} lumens")
    except Exception as e:
        print(f"   Light sensor error: {e}")
    
    sleep(1)
    
    # Test temperature/humidity sensor
    print("\n2. Testing DHT11 (pin 28)...")
    try:
        temp, humidity = get_temperature_humidity()
        print(f"   Temperature: {temp}°C, Humidity: {humidity}%")
    except Exception as e:
        print(f"   DHT11 error: {e}")
    
    sleep(2)  # DHT11 needs more time
    
    # Test ultrasonic sensor
    print("\n3. Testing Ultrasonic Sensor (trigger:21, echo:20)...")
    try:
        distance = get_distance()
        print(f"   Distance: {distance} cm")
    except Exception as e:
        print(f"   Ultrasonic error: {e}")
    
    sleep(1)


def test_all_sensors_combined():
    """Test all sensors together like main.py does"""
    print("\n=== COMBINED SENSOR TEST ===")
    try:
        sensor_data = get_all_sensor_data()
        print(f"Combined data: {sensor_data}")
        return sensor_data
    except Exception as e:
        print(f"Combined sensor error: {e}")
        return None


def main_sensor_test():
    print("Starting sensor-only debug test...")
    print("This tests sensors without OLED or WiFi interference")
    
    # Run tests in loop
    for test_round in range(5):
        print(f"\n{'='*50}")
        print(f"TEST ROUND {test_round + 1}")
        print(f"{'='*50}")
        
        # Test individual sensors
        test_sensors_individually()
        
        # Test combined
        combined_data = test_all_sensors_combined()
        
        print(f"\nRound {test_round + 1} complete. Waiting 3 seconds...")
        sleep(3)
    
    print("\nSensor test complete!")


if __name__ == "__main__":
    try:
        main_sensor_test()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Test error: {e}")
