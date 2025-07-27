# Highcard-SPI IoT Sensor System

## Overview

Highcard-SPI is a comprehensive IoT sensor monitoring system that combines MicroPython-based hardware sensors with a full-stack web application. The system collects real-time sensor data from a Raspberry Pi Pico, transmits it via MQTT, and displays it through a modern web interface with AI-powered analysis capabilities.

## System Architecture

###  Hardware Layer (Pico)
**Location**: `/pico/`

The hardware layer runs on a Raspberry Pi Pico and handles:
- **Sensor Data Collection**: Multiple sensors for environmental monitoring
- **OLED Display**: Real-time status and data visualization
- **WiFi Connectivity**: Wireless communication
- **MQTT Publishing**: Real-time data transmission

**Key Files**:
- `main.py` - Main application entry point with system initialization
- `sensors.py` / `sensors_fast.py` / `sensors_enhanced.py` - Sensor data collection modules
- `oled_display.py` - OLED screen management
- `connections.py` - WiFi and MQTT connectivity
- `system_test.py` - Comprehensive system testing

###  Backend Services
**Location**: `/backend/`

Node.js-based backend that acts as the system hub:
- **MQTT Broker Communication**: Receives sensor data from hardware
- **WebSocket Server**: Real-time data streaming to frontend
- **API Endpoints**: RESTful services for data access
- **Data Processing**: Real-time sensor data processing and storage

**Key Files**:
- `index.js` - Main server application
- `package.json` - Dependencies and scripts

###  Frontend Interface
**Location**: `/frontend/`

React-based web application providing:
- **Real-time Dashboards**: Live sensor data visualization
- **Historical Data Views**: Trend analysis and data history
- **System Controls**: Remote monitoring and configuration
- **Responsive Design**: Multi-device compatibility

###  AI Integration
**Location**: `/AI/`

AI-powered analysis and insights:
- **Data Analysis**: Automated sensor data interpretation
- **Anomaly Detection**: Intelligent monitoring for unusual patterns
- **Predictive Analytics**: Trend-based predictions
- **Voice Integration**: Audio feedback and notifications

**Key Files**:
- `send_to_openai.py` - AI service integration
- `receive.py` - AI response processing

###  Camera System
**Location**: `/Cam_Setup/`

ESP32-based camera module for visual monitoring:
- **Live Video Stream**: Real-time camera feed
- **Image Capture**: Automated photo capture
- **WiFi Streaming**: Wireless video transmission

## Data Flow

```
[Pico Sensors] → [MQTT] → [Backend] → [WebSocket] → [Frontend]
      ↓                      ↓
  [OLED Display]         [AI Analysis]
      ↓                      ↓
  [Local Status]        [Insights & Alerts]
```

1. **Sensor Collection**: Pico continuously reads sensor data
2. **Local Display**: OLED shows current status and readings
3. **Data Transmission**: MQTT publishes data to backend
4. **Processing**: Backend processes and stores data
5. **Real-time Updates**: WebSocket streams data to frontend
6. **AI Analysis**: AI services analyze data for insights
7. **Visualization**: Frontend displays real-time dashboards

## Key Features

###  Sensor Monitoring
- **Multi-sensor Support**: Temperature, humidity, distance, motion detection
- **High-frequency Sampling**: Fast, accurate data collection
- **Quality Assurance**: Built-in sensor validation and calibration
- **Real-time Processing**: Immediate data processing and smoothing

###  Real-time Communication
- **MQTT Protocol**: Lightweight, efficient data transmission
- **WebSocket Streaming**: Instant frontend updates
- **Low Latency**: Optimized for real-time performance
- **Reliable Connectivity**: Auto-reconnection and error handling

###  Web Interface
- **Live Dashboards**: Real-time sensor visualizations
- **Historical Charts**: Time-series data analysis
- **Mobile Responsive**: Works on all devices
- **Modern UI**: Clean, intuitive interface

###  AI-Powered Insights
- **Automated Analysis**: AI interprets sensor patterns
- **Smart Alerts**: Intelligent notification system
- **Predictive Monitoring**: Trend-based predictions
- **Voice Feedback**: Audio status updates

## Getting Started

### Prerequisites
- Raspberry Pi Pico with MicroPython
- Node.js and npm
- MQTT broker (HiveMQ or local)
- WiFi network access

### Hardware Setup
1. Connect sensors to Pico according to pin configuration
2. Flash MicroPython firmware to Pico
3. Upload sensor code to Pico
4. Connect OLED display for local status

### Backend Setup
```bash
cd backend
npm install
npm start
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### AI Services Setup
```bash
cd AI
pip install -r requirements.txt
python send_to_openai.py
```

## File Structure

```
Highcard-SPI/
├── pico/                    # MicroPython hardware code
│   ├── main.py             # Main application
│   ├── sensors_*.py        # Sensor modules
│   ├── oled_display.py     # Display management
│   ├── connections.py      # Connectivity
│   ├── ssd1306.py         # OLED driver
│   ├── debug/             # Debug and diagnostic files
│   ├── tests/             # Testing and validation files
│   ├── fixes/             # Hardware fix implementations
│   └── archive/           # Legacy code and old versions
├── backend/                # Node.js backend
│   ├── index.js           # Main server
│   └── package.json       # Dependencies
├── frontend/              # React frontend
│   ├── src/              # Source code
│   └── package.json      # Dependencies
├── AI/                   # AI services
│   ├── send_to_openai.py # AI integration
│   └── receive.py        # AI processing
└── Cam_Setup/           # Camera system
    └── WifiCam/         # ESP32 camera code
```

## Development

### Testing
- `tests/system_test.py` - Comprehensive system testing
- `tests/sensor_quality_test.py` - Sensor validation
- `tests/distance_speed_test.py` - Performance testing
- `tests/triple_check_verification.py` - Multi-stage verification

### Debugging
- `debug/` folder - Individual component testing files
- Debug modes for sensors and OLED
- MQTT connection testing
- Real-time monitoring tools

## Contributing

This is an IoT sensor monitoring system designed for real-time environmental monitoring with AI-powered insights. The modular architecture allows for easy extension and customization of sensor types, data processing, and visualization capabilities.