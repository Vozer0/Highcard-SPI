from machine import Pin, I2C
import ssd1306
from time import sleep

# Initialize I2C bus 0 with your pins
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)  # Lower frequency

# Scan for I2C devices - for debugging
print("I2C scan:", [hex(addr) for addr in i2c.scan()])

# Add delay before OLED initialization
sleep(0.5)

# Try basic I2C communication test first
try:
    # Test basic communication
    i2c.writeto(0x3C, bytes([0x00, 0xAE]))  # Display off command
    print("Basic I2C communication successful!")
    
    # Create display object for 128x64 display
    oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
    print("OLED initialized successfully!")
    
except Exception as e:
    print(f"Error during OLED setup: {e}")
    # Create a dummy oled object to prevent other errors
    class DummyOled:
        def fill(self, val): pass
        def text(self, text, x, y): pass
        def show(self): pass
    oled = DummyOled()


def wrap_text(text, max_width, oled, line_height=10):
    """
    Wrap text to fit OLED display width in pixels,
    and print line-by-line moving down by line_height pixels.
    """
    oled.fill(0)  # Clear display
    x, y = 0, 0

    words = text.split(' ')
    line = ''

    for word in words:
        test_line = line + (' ' if line else '') + word
        
        # Approximate text width: each char ~8 pixels
        width = len(test_line) * 8

        if width > max_width:
            # Print current line and move down
            if line:  # Only print if line has content
                oled.text(line, x, y)
                y += line_height
                
            # Check if we've exceeded display height
            if y >= 64:
                break
                
            line = word  # start new line with current word
        else:
            line = test_line

    # Print any leftover text if there's space
    if line and y < 64:
        oled.text(line, x, y)
    
    oled.show()


def display_text(message):
    """
    Simple function to display text on OLED
    """
    print(f"Displaying on OLED: {message}")
    wrap_text(message, 128, oled)


def clear_display():
    """
    Clear the OLED display
    """
    oled.fill(0)
    oled.show()


# Example usage - only run if this file is executed directly
if __name__ == "__main__":
    try:
        while True:
            user_text = input("Enter message (Ctrl+C to exit): ")
            if user_text.lower() == 'clear':
                clear_display()
            else:
                display_text(user_text)
    except KeyboardInterrupt:
        print("\nExiting...")
        clear_display()
