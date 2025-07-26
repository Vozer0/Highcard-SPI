from machine import Pin, I2C
import ssd1306
from time import sleep

def fix_i2c_timeout():
    """
    Fix for I2C timeout issues
    """
    print("=== FIXING I2C TIMEOUT ISSUE ===")
    
    # Test different I2C frequencies (start very low)
    frequencies = [10000, 50000, 100000, 200000]
    
    for freq in frequencies:
        print(f"\nTrying I2C frequency: {freq}Hz")
        try:
            # Initialize I2C with lower frequency
            i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=freq)
            
            # Scan for devices first
            print("Scanning I2C bus...")
            devices = i2c.scan()
            print(f"Found devices: {[hex(addr) for addr in devices]}")
            
            if 0x3C not in devices:
                print(f"OLED not found at {freq}Hz")
                continue
            
            # Try basic communication
            print("Testing basic I2C communication...")
            i2c.writeto(0x3C, bytes([0x00, 0xAE]))  # Display off command
            print("Basic communication OK!")
            
            # Try initializing OLED
            print("Initializing OLED...")
            oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
            print("OLED initialized successfully!")
            
            # Test simple operations
            print("Testing simple fill...")
            oled.fill(0)
            oled.show()
            print("Black fill OK!")
            
            sleep(1)
            
            print("Testing white fill...")
            oled.fill(1)
            oled.show()
            print("White fill OK!")
            
            sleep(2)
            
            # Test text
            print("Testing text...")
            oled.fill(0)
            oled.text("SUCCESS!", 0, 0, 1)
            oled.text(f"Freq:{freq}", 0, 10, 1)
            oled.show()
            print("Text display OK!")
            
            sleep(3)
            
            print(f"SUCCESS! Working frequency: {freq}Hz")
            return oled, i2c, freq
            
        except OSError as e:
            print(f"Failed at {freq}Hz: {e}")
            continue
        except Exception as e:
            print(f"Other error at {freq}Hz: {e}")
            continue
    
    print("All frequencies failed. Check wiring!")
    return None, None, None

def test_working_display(oled):
    """
    Test the working display
    """
    if oled is None:
        print("No working display found!")
        return
    
    print("\n=== TESTING WORKING DISPLAY ===")
    
    # Clear test
    oled.fill(0)
    oled.show()
    sleep(1)
    
    # Text test
    oled.fill(0)
    oled.text("Hello World!", 0, 0, 1)
    oled.text("Line 2", 0, 12, 1)
    oled.text("Line 3", 0, 24, 1)
    oled.show()
    sleep(3)
    
    # Pattern test
    oled.fill(0)
    for i in range(0, 128, 8):
        oled.pixel(i, 10, 1)
        oled.pixel(i, 20, 1)
        oled.pixel(i, 30, 1)
    oled.show()
    sleep(2)
    
    print("Display test complete!")

def main():
    print("Starting I2C timeout fix...")
    print("This will test different I2C frequencies to find one that works.")
    print()
    
    oled, i2c, freq = fix_i2c_timeout()
    
    if oled:
        print(f"\nFound working configuration with {freq}Hz")
        test_working_display(oled)
        
        print("\nRecommendation:")
        print(f"Update your oled_display.py to use freq={freq}")
        print("Change this line:")
        print("i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)")
        print("To:")
        print(f"i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq={freq})")
    else:
        print("\nNo working frequency found. Possible issues:")
        print("1. Check wiring - SDA to pin 8, SCL to pin 9")
        print("2. Check power - 3.3V and GND connections")
        print("3. Try adding pull-up resistors (4.7k ohm)")
        print("4. Check for loose connections")

if __name__ == "__main__":
    main()
