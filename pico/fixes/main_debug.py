from oled_debug import debug_oled
from time import sleep

def main():
    print("Starting OLED debug session...")
    print("Watch your OLED screen carefully and note what you see for each test!")
    print()
    
    # Run the comprehensive debug
    debug_oled()
    
    print()
    print("Debug complete! Please tell me:")
    print("1. Which tests showed something on the screen?")
    print("2. What exactly did you see (white screen, dots, text, etc.)?")
    print("3. Were any characters readable?")

if __name__ == "__main__":
    main()
