from machine import Pin, I2C
import ssd1306
from time import sleep

def targeted_debug():
    """
    Focused debug for the dots issue
    """
    print("=== TARGETED OLED DEBUG ===")
    
    # Initialize
    i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)
    oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
    
    # Test 1: Check what fill(1) actually does
    print("Test 1: Basic fill test")
    oled.fill(1)
    oled.show()
    print("Should see solid white - do you see dots?")
    sleep(3)
    
    # Test 2: Manual pixel filling
    print("Test 2: Manual pixel fill")
    oled.fill(0)  # Clear first
    # Fill every pixel manually
    for x in range(128):
        for y in range(64):
            oled.pixel(x, y, 1)
    oled.show()
    print("Manual pixel fill - solid white or still dots?")
    sleep(3)
    
    # Test 3: Partial fills
    print("Test 3: Partial area fill")
    oled.fill(0)
    # Fill just a rectangle
    for x in range(20, 60):
        for y in range(10, 30):
            oled.pixel(x, y, 1)
    oled.show()
    print("Rectangle fill - solid rectangle or dots?")
    sleep(3)
    
    # Test 4: Line drawing
    print("Test 4: Line drawing")
    oled.fill(0)
    # Draw horizontal lines
    for y in range(0, 64, 4):
        for x in range(128):
            oled.pixel(x, y, 1)
    oled.show()
    print("Horizontal lines - solid lines or dots?")
    sleep(3)
    
    # Test 5: Different display initialization
    print("Test 5: Reinitializing display")
    try:
        # Try different initialization
        oled2 = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
        oled2.invert(1)  # Try inverted
        oled2.fill(0)
        oled2.show()
        sleep(1)
        oled2.invert(0)  # Back to normal
        oled2.fill(1)
        oled2.show()
        print("Reinitialized display - better?")
        sleep(3)
    except:
        print("Reinit failed")
    
    # Test 6: Check framebuffer directly
    print("Test 6: Framebuffer inspection")
    oled.fill(1)
    print(f"Framebuffer width: {oled.width}")
    print(f"Framebuffer height: {oled.height}")
    # Check a few bytes of the buffer
    try:
        buffer_sample = bytes(oled.framebuf.buf[:10])
        print(f"First 10 buffer bytes: {[hex(b) for b in buffer_sample]}")
    except:
        print("Could not read buffer")
    oled.show()
    sleep(2)
    
    print("=== DEBUG COMPLETE ===")

if __name__ == "__main__":
    targeted_debug()
