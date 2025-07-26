
import openai
import base64
import os
import json
from gtts import gTTS
import pygame
import io
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Initialize OpenAI client
client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

if not os.getenv('OPENAI_API_KEY'):
    print("Error: OPENAI_API_KEY environment variable not set")
    print("Please add your OpenAI API key to the .env file")
    sys.exit(1)

# Image encoding, code provided
def encode_image(image_path):
    with open(image_path, "rb") as image_F:
        return base64.b64encode(image_F.read()).decode('utf-8')

# Sending a request and getting a response
def analyze_image_with_openai(image_path, prompt="Analyze this image and describe what you see in detail."):
    try:
        # Encode the image
        base64_image = encode_image(image_path)
        
        # Create the API request using the new client
        response = client.chat.completions.create(
            model="gpt-4o",  # Updated to use gpt-4o which supports vision
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        # Extract the response text
        description = response.choices[0].message.content
        print("OpenAI Analysis:", description)
        return description
        
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

# How do we make things audible?
def text_to_speech(text, output_file="description.wav"):
    try:
        # Create TTS object
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Save to a BytesIO object first
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Save to file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        audio_path = os.path.join(script_dir, "../backend", output_file)
        
        with open(audio_path, "wb") as f:
            f.write(audio_buffer.read())
        
        print(f"Audio saved to: {audio_path}")
        
        # Play the audio
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        
        # Wait for audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
            
        return audio_path
        
    except Exception as e:
        print(f"Error creating audio: {e}")
        return None

# Can we put everything together?
def complete_image_analysis(image_path, custom_prompt=None):
    """
    Complete pipeline: analyze image with OpenAI and return text description
    """
    default_prompt = ("Analyze this image and provide a detailed description. "
                     "Focus on objects, people, activities, and the overall scene. "
                     "Keep the description clear and informative.")
    
    prompt = custom_prompt if custom_prompt else default_prompt
    
    print("Starting image analysis...")
    
    # Analyze the image
    description = analyze_image_with_openai(image_path, prompt)
    
    if description:
        print("Analysis completed successfully!")
        print(f"Description: {description}")
        
        return {
            "success": True,
            "description": description,
            "audio_path": None  # No audio generation needed
        }
    else:
        return {
            "success": False,
            "description": None,
            "audio_path": None
        }

if __name__ == "__main__":
    # Test the functions
    test_image = "../frontend/src/downloaded_image.jpg"
    if os.path.exists(test_image):
        result = complete_image_analysis(test_image)
        print("Analysis result:", result)
    else:
        print("Test image not found")

