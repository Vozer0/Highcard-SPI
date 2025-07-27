import React, { useState, useEffect } from "react";
import io from 'socket.io-client';
import './App.css';

const socket = io('http://localhost:8000');

function App() {
  const [pictureStatus, setPictureStatus] = useState("");
  const [displayText, setDisplayText] = useState("");
  const [sendStatus, setSendStatus] = useState("");
  const [aiDescription, setAiDescription] = useState(""); // New state for AI description
  
  
  const [sensorData, setSensorData] = useState({
    temperature: 'Loading...',
    humidity: 'Loading...',
    light: 'Loading...',
    ultrasonic: 'Loading...',
    lastUpdated: null
  });

  useEffect(() => {
    socket.on('connect', () => console.log('Connected:', socket.id));
    
    socket.on('picture_taken', data => {
      setPictureStatus(data.message);
      if (data.success && data.description) {
        setAiDescription(data.description);
      }
      setTimeout(() => setPictureStatus(""), 3000);
    });

    
    // Real-time sensor data handlers - always update to latest value
    socket.on('temp', (data) => {
      setSensorData(prev => ({ 
        ...prev, 
        temperature: data,
        lastUpdated: new Date().toLocaleTimeString()
      }));
      console.log(`🌡️ Temperature updated: ${data}°C`);
    });

    socket.on('humidity', (data) => {
      setSensorData(prev => ({ 
        ...prev, 
        humidity: data,
        lastUpdated: new Date().toLocaleTimeString()
      }));
      console.log(`💧 Humidity updated: ${data}%`);
    });

    socket.on('light', (data) => {
      setSensorData(prev => ({ 
        ...prev, 
        light: data,
        lastUpdated: new Date().toLocaleTimeString()
      }));
      console.log(`💡 Light updated: ${data}`);
    });

    socket.on('ultrasonic', (data) => {
      setSensorData(prev => ({ 
        ...prev, 
        ultrasonic: data,
        lastUpdated: new Date().toLocaleTimeString()
      }));
      console.log(`📏 Distance updated: ${data}cm`);
    });

    return () => {
      socket.off('picture_taken');
      socket.off('temp');
      socket.off('humidity');
      socket.off('light');
      socket.off('ultrasonic');
    };
  }, []);

  const handleSendText = () => {
    if (displayText.trim()) {
      socket.emit('display', displayText);
      setSendStatus("Text sent to OLED!");
      setTimeout(() => setSendStatus(""), 2000); 
    } else {
      setSendStatus("Please enter some text!");
      setTimeout(() => setSendStatus(""), 2000);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendText();
    }
  };

  const handleTakePicture = () => {
    setPictureStatus("Taking picture and analyzing...");
    socket.emit('take_picture');
  };

  return (
    <div className="app">
      {/* Sensor Readings Section */}
      <div className="sensors-grid">
        <div className="sensor-box">
          <div className="sensor-label">Temperature</div>
          <div className="sensor-value">
            {sensorData.temperature !== 'Loading...' ? `${sensorData.temperature}°C` : 'Loading...'}
          </div>
          <div className="sensor-timestamp">
            {sensorData.lastUpdated && `Updated: ${sensorData.lastUpdated}`}
          </div>
        </div>

        <div className="sensor-box">
          <div className="sensor-label">Humidity</div>
          <div className="sensor-value">
            {sensorData.humidity !== 'Loading...' ? `${sensorData.humidity}%` : 'Loading...'}
          </div>
          <div className="sensor-timestamp">
            {sensorData.lastUpdated && `Updated: ${sensorData.lastUpdated}`}
          </div>
        </div>

        <div className="sensor-box">
          <div className="sensor-label">Light Level</div>
          <div className="sensor-value">
            {sensorData.light !== 'Loading...' ? sensorData.light : 'Loading...'}
          </div>
          <div className="sensor-timestamp">
            {sensorData.lastUpdated && `Updated: ${sensorData.lastUpdated}`}
          </div>
        </div>

        <div className="sensor-box">
          <div className="sensor-label">Distance</div>
          <div className="sensor-value">
            {sensorData.ultrasonic !== 'Loading...' ? `${sensorData.ultrasonic} cm` : 'Loading...'}
          </div>
          <div className="sensor-timestamp">
            {sensorData.lastUpdated && `Updated: ${sensorData.lastUpdated}`}
          </div>
        </div>
      </div>

      <div className="text-display-container">
        <h2>Send Text to OLED Display</h2>
        
        <div className="input-group">
          <input
            type="text"
            value={displayText}
            onChange={(e) => setDisplayText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter text to display on OLED..."
            className="text-input"
            maxLength={100}
          />
          <button 
            onClick={handleSendText}
            className="send-button"
            disabled={!displayText.trim()}
          >
            Send to OLED
          </button>
        </div>

        {sendStatus && (
          <div className={`status-message ${sendStatus.includes('sent') ? 'success' : 'error'}`}>
            {sendStatus}
          </div>
        )}

        <div className="current-text">
          <p><strong>Current text:</strong> {displayText || "No text entered"}</p>
        </div>
      </div>

      {/* AI Camera Analysis Section */}
      <div className="camera-container">
        <h2>ESP32 Camera AI Analysis</h2>
        <p>Take a picture with your ESP32 camera and get an AI description</p>
        
        <button 
          onClick={handleTakePicture}
          className="camera-button"
          disabled={pictureStatus && pictureStatus.includes('Taking')}
        >
          📸 Take Picture & Analyze
        </button>

        {pictureStatus && (
          <div className={`status-message ${pictureStatus.includes('successfully') ? 'success' : pictureStatus.includes('Taking') ? 'info' : 'error'}`}>
            {pictureStatus}
          </div>
        )}

        {/* AI Description Display */}
        {aiDescription && (
          <div className="ai-description-container">
            <h3>🤖 AI Analysis Result:</h3>
            <div className="ai-description-text">
              {aiDescription}
            </div>
            <button 
              onClick={() => setAiDescription("")}
              className="clear-description-button"
            >
              Clear Description
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
