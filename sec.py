"""
Secure API Key Storage Examples
"""
import os

# Method 1: Using environment variables (RECOMMENDED)
# Set in your terminal: set OPENAI_API_KEY=your-actual-key-here
API_KEY = os.getenv('OPENAI_API_KEY')

# Method 2: If environment variable not set, provide a placeholder
if not API_KEY:
    print("Warning: OPENAI_API_KEY environment variable not set!")
    print("Please set it using: $env:OPENAI_API_KEY = 'your-api-key-here'")
    # API_KEY = "your-api-key-here"  # Uncomment and replace for testing only

# Method 3: Load from a separate config file (create config.py and add to .gitignore)
# try:
#     from config import OPENAI_API_KEY as API_KEY
# except ImportError:
#     print("config.py not found - using environment variable")

def get_api_key():
    """Function to safely get the API key"""
    if not API_KEY:
        raise ValueError("API key not configured. Please set OPENAI_API_KEY environment variable.")
    return API_KEY