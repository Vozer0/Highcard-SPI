#!/usr/bin/env python3
"""
Helper script to update ESP32 IP address in receive.py
"""
import os
import sys

def update_esp32_ip():
    """Interactive script to update ESP32 IP address"""
    receive_py_path = os.path.join(os.path.dirname(__file__), 'receive.py')
    
    # Read current file
    with open(receive_py_path, 'r') as f:
        content = f.read()
    
    # Find current IP
    lines = content.split('\n')
    current_ip = None
    line_number = None
    
    for i, line in enumerate(lines):
        if 'url = "http://' in line and '/1024x768.jpg"' in line:
            current_ip = line.split('http://')[1].split('/1024x768.jpg')[0]
            line_number = i
            break
    
    if current_ip:
        print(f"Current ESP32 IP address: {current_ip}")
    else:
        print("Could not find current IP address in receive.py")
        return False
    
    # Get new IP from user
    print("\nTo find your ESP32 IP address:")
    print("1. Open Arduino IDE")
    print("2. Connect to your ESP32")
    print("3. Open Serial Monitor")
    print("4. Look for the IP address when ESP32 connects to WiFi")
    print()
    
    new_ip = input("Enter your ESP32's IP address (or press Enter to keep current): ").strip()
    
    if not new_ip:
        print("No changes made.")
        return True
    
    # Validate IP format (basic check)
    if not new_ip.replace('.', '').replace(':', '').isdigit():
        print("Invalid IP format. Please enter a valid IP address.")
        return False
    
    # Update the file
    old_line = f'url = "http://{current_ip}/1024x768.jpg"'
    new_line = f'url = "http://{new_ip}/1024x768.jpg"'
    
    updated_content = content.replace(old_line, new_line)
    
    with open(receive_py_path, 'w') as f:
        f.write(updated_content)
    
    print(f"✅ Updated ESP32 IP address from {current_ip} to {new_ip}")
    print("You can now test the AI system!")
    return True

if __name__ == "__main__":
    success = update_esp32_ip()
    sys.exit(0 if success else 1)
