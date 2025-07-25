
import requests
import os
import sys
from send_to_openai import complete_image_analysis

# Get the folder where the script is located, done for you
script_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(script_dir, "../frontend/src/downloaded_image.jpg") 

url = "http://172.20.10.6/1024x768.jpg"             # You will have to change the IP Address

# Function to download the image from esp32, given to you
def download_image():
    try:
        print("Downloading image from ESP32...")
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            # Ensure directory exists
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Image saved to: {filename}")
            return True
        else:
            print("Failed to download image. Status code:", response.status_code)
            return False
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False

# Download the image and get a response from openai
def analyze_esp32_image():
    """
    Complete pipeline: Download image from ESP32, analyze with OpenAI, and create audio
    """
    print("Starting ESP32 image analysis pipeline...")
    
    # Step 1: Download the image
    if not download_image():
        print("Failed to download image from ESP32")
        return False
    
    # Step 2: Analyze with OpenAI
    print("Analyzing image with OpenAI...")
    result = complete_image_analysis(filename)
    
    if result["success"]:
        print("Analysis completed successfully!")
        print("Description:", result["description"])
        if result["audio_path"]:
            print("Audio description created and played!")
        return True
    else:
        print("Analysis failed")
        return False

# Control when to take photo - can be called from command line or other scripts
def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "get_description":
            success = analyze_esp32_image()
            sys.exit(0 if success else 1)
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
    else:
        # Default behavior - just download and analyze
        analyze_esp32_image()

if __name__ == "__main__":
    main()

