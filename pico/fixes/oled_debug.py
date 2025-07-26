from machine import Pin, I2C
import ssd1306
from time import sleep

# Debug version for OLED troubleshooting

def debug_oled():
    """
    Comprehensive OLED debugging function
    """
    print("=== OLED DEBUG MODE ===")
    
    # Initialize I2C
    print("1. Initializing I2C...")
    i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)
    
    # Scan for devices
    print("2. Scanning I2C bus...")
    devices = i2c.scan()
    print(f"Found devices: {[hex(addr) for addr in devices]}")
    
    if 0x3C not in devices:
        print("ERROR: OLED not found at address 0x3C!")
        return False
    
    # Initialize OLED
    print("3. Initializing OLED...")
    try:
        oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
        print("OLED initialized successfully!")
    except Exception as e:
        print(f"ERROR initializing OLED: {e}")
        return False
    
    # Test 1: Fill tests
    print("4. Testing screen fill...")
    try:
        print("  - Filling white...")
        oled.fill(1)
        oled.show()
        sleep(2)
        
        print("  - Filling black...")
        oled.fill(0)
        oled.show()
        sleep(1)
        print("  Fill test completed!")
    except Exception as e:
        print(f"  ERROR in fill test: {e}")
    
    # Test 2: Pixel tests
    print("5. Testing individual pixels...")
    try:
        oled.fill(0)
        # Draw a pattern
        for x in range(0, 128, 8):
            for y in range(0, 64, 8):
                oled.pixel(x, y, 1)
        oled.show()
        sleep(2)
        print("  Pixel test completed!")
    except Exception as e:
        print(f"  ERROR in pixel test: {e}")
    
    # Test 3: Text tests with different parameters
    print("6. Testing text rendering...")
    try:
        # Test 3a: Simple text
        oled.fill(0)
        oled.text("A", 0, 0, 1)
        oled.show()
        sleep(1)
        print("  Single character 'A' displayed")
        
        # Test 3b: Multiple characters
        oled.fill(0)
        oled.text("ABC", 0, 0, 1)
        oled.show()
        sleep(1)
        print("  'ABC' displayed")
        
        # Test 3c: Full word
        oled.fill(0)
        oled.text("Hello", 0, 0, 1)
        oled.show()
        sleep(1)
        print("  'Hello' displayed")
        
        # Test 3d: Multiple lines
        oled.fill(0)
        oled.text("Line1", 0, 0, 1)
        oled.text("Line2", 0, 10, 1)
        oled.text("Line3", 0, 20, 1)
        oled.show()
        sleep(2)
        print("  Multiple lines displayed")
        
        # Test 3e: Different positions
        oled.fill(0)
        oled.text("TL", 0, 0, 1)      # Top-left
        oled.text("TR", 96, 0, 1)     # Top-right
        oled.text("BL", 0, 50, 1)     # Bottom-left
        oled.text("BR", 96, 50, 1)    # Bottom-right
        oled.text("CTR", 40, 25, 1)   # Center
        oled.show()
        sleep(3)
        print("  Position test completed")
        
    except Exception as e:
        print(f"  ERROR in text test: {e}")
    
    # Test 4: Contrast tests
    print("7. Testing contrast levels...")
    try:
        oled.fill(0)
        oled.text("Contrast Test", 0, 0, 1)
        
        for contrast in [50, 100, 150, 200, 255]:
            print(f"  Setting contrast to {contrast}")
            oled.contrast(contrast)
            oled.show()
            sleep(1)
            
    except Exception as e:
        print(f"  ERROR in contrast test: {e}")
    
    # Test 5: Large text simulation
    print("8. Testing large text...")
    try:
        oled.fill(0)
        oled.contrast(255)
        # Draw large "H" manually using pixels
        for y in range(10, 30):
            oled.pixel(10, y, 1)  # Left line
            oled.pixel(20, y, 1)  # Right line
        for x in range(10, 21):
            oled.pixel(x, 20, 1)  # Middle line
        oled.show()
        sleep(2)
        print("  Large 'H' drawn with pixels")
    except Exception as e:
        print(f"  ERROR in large text test: {e}")
    
    print("=== DEBUG COMPLETE ===")
    return True

if __name__ == "__main__":
    debug_oled()
