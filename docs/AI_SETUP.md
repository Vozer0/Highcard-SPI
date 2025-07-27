# ESP32 Camera AI Analysis Setup

## Overview
This system captures images from an ESP32 camera, analyzes them using OpenAI's GPT-4 Vision API, and provides audio descriptions using text-to-speech.

## Prerequisites
1. **ESP32 Camera** - Set up and connected to your network
2. **OpenAI API Key** - Get one from https://platform.openai.com/
3. **Python Dependencies** - Already installed via requirements.txt

## Setup Instructions

### 1. Configure Environment Variables
1. Copy `.env.example` to `.env`
2. Add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

### 2. Update ESP32 Camera IP Address
Edit `AI/receive.py` and update the URL to your ESP32's IP address:
```python
url = "http://YOUR_ESP32_IP_ADDRESS/1024x768.jpg"
```

### 3. Test the System

#### Test Image Download:
```bash
cd AI
python receive.py
```

#### Test OpenAI Analysis:
```bash
cd AI
python send_to_openai.py
```

#### Test Full Pipeline:
```bash
cd AI
python receive.py get_description
```

### 4. Run the Application

#### Start Backend:
```bash
cd backend
npm install
node index.js
```

#### Start Frontend:
```bash
cd frontend
npm install
npm start
```

## How It Works

1. **Frontend**: Click "Take Picture & Analyze" button
2. **Backend**: Receives request and calls Python script
3. **Python Script**: 
   - Downloads image from ESP32 camera
   - Sends image to OpenAI GPT-4 Vision API
   - Gets detailed description
   - Converts description to speech using gTTS
   - Plays audio description
4. **Frontend**: Shows success/error status

## Features

- **Real-time Sensor Data**: Temperature, humidity, light, and ultrasonic sensors
- **Text to OLED**: Send custom text to connected OLED display
- **AI Image Analysis**: Take pictures and get detailed AI descriptions
- **Audio Feedback**: Hear the image description spoken aloud
- **Responsive Design**: Works on desktop and mobile

## Troubleshooting

### Common Issues:

1. **"Failed to download image"**
   - Check ESP32 IP address in `AI/receive.py`
   - Ensure ESP32 is connected to network
   - Try accessing the URL directly in browser

2. **"OpenAI API Error"**
   - Verify your API key is correct in `.env`
   - Check you have credits in your OpenAI account
   - Ensure the image file exists and is valid

3. **"Audio not playing"**
   - Check that pygame is installed correctly
   - Ensure your system has audio output enabled
   - Try running the script with admin privileges

4. **"Python script failed"**
   - Check that all dependencies are installed
   - Verify Python path in backend (may need `python3` instead of `python`)
   - Check console output for specific error messages

## ESP32 Camera Requirements

Your ESP32 should serve images at the endpoint:
- Format: JPEG
- Resolution: 1024x768 (or adjust URL in receive.py)
- Accessible via HTTP GET request

Example ESP32 endpoint: `http://192.168.1.100/1024x768.jpg`
