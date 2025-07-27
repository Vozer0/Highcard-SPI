from machine import Pin, I2C
import ssd1306
from time import sleep

# Initialize I2C bus 0 with your working pins
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=200000)  # Back to working configuration

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
    
    # Test the display immediately
    oled.fill(0)
    oled.text("INIT OK", 0, 0, 1)
    oled.show()
    sleep(1)
    
except Exception as e:
    print(f"Error during OLED setup: {e}")
    # Create a dummy oled object to prevent other errors
    class DummyOled:
        def fill(self, val): pass
        def text(self, text, x, y, col=1): pass
        def show(self): pass
        def contrast(self, val): pass
    oled = DummyOled()


def wrap_text(text, max_width, oled, line_height=12):
    """
    Wrap text to fit OLED display width in pixels,
    and print line-by-line moving down by line_height pixels.
    Updated for better visibility.
    """
    oled.fill(0)  # Clear display
    oled.contrast(255)  # Set maximum contrast
    x, y = 0, 0

    words = text.split(' ')
    line = ''
    
    # Each character is about 8 pixels wide in the default font
    max_chars_per_line = max_width // 8

    for word in words:
        test_line = line + (' ' if line else '') + word
        
        if len(test_line) > max_chars_per_line:
            # Print current line and move down
            if line:  # Only print if line has content
                oled.text(line, x, y, 1)  # Make sure color is 1 (white)
                y += line_height
                
            # Check if we've exceeded display height
            if y >= 64:
                break
                
            line = word  # start new line with current word
        else:
            line = test_line

    # Print any leftover text if there's space
    if line and y < 64:
        oled.text(line, x, y, 1)  # Make sure color is 1 (white)
    
    oled.show()


def display_text(message):
    """
    Simple function to display text on OLED with better visibility
    """
    print(f"Displaying on OLED: {message}")
    
    try:
        # Set maximum contrast for better visibility
        oled.contrast(255)
        
        # Test with simple direct text first
        oled.fill(0)  # Clear with black
        
        # Break message into lines that fit
        lines = []
        words = message.split(' ')
        current_line = ''
        
        for word in words:
            test_line = current_line + (' ' if current_line else '') + word
            if len(test_line) <= 16:  # About 16 chars per line for 128px width
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Display lines with spacing
        for i, line in enumerate(lines[:5]):  # Max 5 lines for 64px height
            oled.text(line, 0, i * 12, 1)  # White text
        
        oled.show()
        
    except Exception as e:
        print(f"Error displaying text: {e}")


def clear_display():
    """
    Clear the OLED display
    """
    try:
        oled.fill(0)
        oled.show()
    except Exception as e:
        print(f"Error clearing display: {e}")


def test_display():
    """
    Test function to check if display is working properly
    """
    try:
        print("Testing OLED display...")
        
        # Test 1: Fill screen white
        oled.fill(1)
        oled.show()
        sleep(1)
        
        # Test 2: Fill screen black
        oled.fill(0)
        oled.show()
        sleep(1)
        
        # Test 3: Draw some pixels
        oled.fill(0)
        for i in range(0, 128, 10):
            oled.pixel(i, 10, 1)
        oled.show()
        sleep(1)
        
        # Test 4: Simple text
        oled.fill(0)
        oled.text("Hello", 0, 0, 1)
        oled.text("World", 0, 10, 1)
        oled.text("Test", 0, 20, 1)
        oled.show()
        sleep(2)
        
        # Test 5: Large text simulation (using multiple characters)
        oled.fill(0)
        oled.text("BIG", 30, 25, 1)
        oled.show()
        
        print("Display test complete!")
        
    except Exception as e:
        print(f"Error in test_display: {e}")


# Example usage - only run if this file is executed directly
if __name__ == "__main__":
    try:
        # Run test first
        test_display()
        sleep(2)
        
        while True:
            user_text = input("Enter message ('test' for test, 'clear' to clear, Ctrl+C to exit): ")
            if user_text.lower() == 'clear':
                clear_display()
            elif user_text.lower() == 'test':
                test_display()
            else:
                display_text(user_text)
    except KeyboardInterrupt:
        print("\nExiting...")
        clear_display()
