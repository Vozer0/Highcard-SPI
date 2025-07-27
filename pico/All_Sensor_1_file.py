from machine import Pin, I2C
import ssd1306
import time
import dht


from machine import  PWM, ADC
from time import sleep, sleep_ms, sleep_us



trigger = Pin(21,Pin.OUT)
echo = Pin(20,Pin.IN)
sensor = dht.DHT11(Pin(28)) 
ldr = ADC(Pin(26))
def lumens():
    raw = ldr.read_u16() 
    voltage = raw * 3.3 / 65535
    
    lumenVal = (.344*voltage) -.148
    #lumensVal = (.355*voltage) -.155
    return str(lumenVal)
    
    #return str( "Lumens: " + lumensVal)


def humAndTemp():
    
    
   
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
               
        
        #print(f"Temperature: {temp}'C, Humidity: {hum}%")
        return (sensor.temperature(),      # temp  (int) or None
                sensor.humidity()) 
        
    except Exception as e:
        return(None,None)
        
  

def ultra():
    signaloff = 0
    signalon = 0

    trigger.low()
    time.sleep_us(2)
    trigger.high()
    time.sleep_us(5)
    trigger.low()

    while echo.value() == 0:
        signaloff = time.ticks_us()
    while echo.value() == 1:
        signalon = time.ticks_us()
    timepassed = signalon - signaloff

    distance =  (timepassed * .0343)/2
    distance = "{:.1f}".format(distance)

    #print (distance + " cm")
    return str(distance + " cm")





# Initialize I2C bus 1 with your pins
i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=400000)

# Create display object for 128x64 display
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)




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
   


# Example usage - only run if this file is executed directly
if __name__ == "__main__":
    try:
        while True:
            
        #sleep(2)
            
            #display_text(ultra())
            #print("lumens " + lumens())
           
            
           
       
           
            
            
            temp, hum = humAndTemp()   # ➋  tuple unpacking
            temp = temp if temp is not None else -1
            hum  = hum  if hum  is not None else -1
           
           
            
            sleep(.5)
            
           
    except KeyboardInterrupt:
        print("\nExiting...")
        clear_display()
