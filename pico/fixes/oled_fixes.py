from machine import Pin, I2C
import ssd1306
from time import sleep

def fixed_oled_test():
    """
    Potential fix for the dots issue
    """
    print("=== TRYING OLED FIXES ===")
    
    # Initialize with different settings
    i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)  # Try higher frequency
    
    print("Fix 1: Higher I2C frequency")
    oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
    
    # Force proper initialization sequence
    oled.poweroff()
    sleep(0.1)
    oled.poweron()
    oled.init_display()
    
    # Test
    oled.fill(1)
    oled.show()
    print("Higher freq test - solid white?")
    sleep(3)
    
    print("Fix 2: Manual display configuration")
    # Try manual configuration
    oled.write_cmd(0xAE)  # Display off
    oled.write_cmd(0xD5)  # Set display clock divide ratio/oscillator frequency
    oled.write_cmd(0x80)  # Default
    oled.write_cmd(0xA8)  # Set multiplex ratio
    oled.write_cmd(0x3F)  # 64 lines
    oled.write_cmd(0xD3)  # Set display offset
    oled.write_cmd(0x00)  # No offset
    oled.write_cmd(0x40)  # Set start line address
    oled.write_cmd(0x8D)  # Charge pump setting
    oled.write_cmd(0x14)  # Enable charge pump
    oled.write_cmd(0x20)  # Memory addressing mode
    oled.write_cmd(0x00)  # Horizontal addressing mode
    oled.write_cmd(0xA1)  # Set segment re-map
    oled.write_cmd(0xC8)  # Set COM output scan direction
    oled.write_cmd(0xDA)  # Set COM pins hardware configuration
    oled.write_cmd(0x12)  # 
    oled.write_cmd(0x81)  # Set contrast control
    oled.write_cmd(0xFF)  # Maximum contrast
    oled.write_cmd(0xD9)  # Set pre-charge period
    oled.write_cmd(0xF1)  # 
    oled.write_cmd(0xDB)  # Set VCOMH deselect level
    oled.write_cmd(0x40)  # 
    oled.write_cmd(0xA4)  # Entire display on (normal)
    oled.write_cmd(0xA6)  # Set normal display (not inverted)
    oled.write_cmd(0xAF)  # Display on
    
    sleep(0.1)
    oled.fill(1)
    oled.show()
    print("Manual config test - solid white?")
    sleep(3)
    
    print("Fix 3: Different framebuffer approach")
    oled.fill(0)
    # Try writing directly to framebuffer
    try:
        # Fill framebuffer with 0xFF (all pixels on)
        for i in range(len(oled.framebuf.buf)):
            oled.framebuf.buf[i] = 0xFF
        oled.show()
        print("Direct framebuffer write - solid white?")
        sleep(3)
    except Exception as e:
        print(f"Direct write failed: {e}")
    
    print("Fix 4: Test simple patterns")
    oled.fill(0)
    # Checkerboard pattern
    for x in range(0, 128, 2):
        for y in range(0, 64, 2):
            oled.pixel(x, y, 1)
            oled.pixel(x+1, y+1, 1)
    oled.show()
    print("Checkerboard pattern - what do you see?")
    sleep(3)
    
    # Vertical stripes
    oled.fill(0)
    for x in range(0, 128, 4):
        for y in range(64):
            oled.pixel(x, y, 1)
            oled.pixel(x+1, y, 1)
    oled.show()
    print("Vertical stripes - solid stripes or dots?")
    sleep(3)
    
    print("=== FIXES COMPLETE ===")

if __name__ == "__main__":
    fixed_oled_test()
