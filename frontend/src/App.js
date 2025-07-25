import React, { useState, useEffect } from "react";
import io from 'socket.io-client';
import './App.css';

const socket = io('http://localhost:8000');

function App() {
  const [pictureStatus, setPictureStatus] = useState("");
  const [displayText, setDisplayText] = useState("");
  const [sendStatus, setSendStatus] = useState("");
  
  
  const [sensorData, setSensorData] = useState({
    temperature: null,
    humidity: null,
    light: null,
    ultrasonic: null
  });

  useEffect(() => {
    socket.on('connect', () => console.log('Connected:', socket.id));
    
    socket.on('picture_taken', data => {
      setPictureStatus(data.message);
      setTimeout(() => setPictureStatus(""), 3000);
    });

    
    socket.on('temp', (data) => {
      setSensorData(prev => ({ ...prev, temperature: data }));
    });

    socket.on('humidity', (data) => {
      setSensorData(prev => ({ ...prev, humidity: data }));
    });

    socket.on('light', (data) => {
      setSensorData(prev => ({ ...prev, light: data }));
    });

    socket.on('ultrasonic', (data) => {
      setSensorData(prev => ({ ...prev, ultrasonic: data }));
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

  return (
    <div className="app">
      {/* Sensor Readings Section */}
      <div className="sensors-grid">
        <div className="sensor-box temperature">
          <div className="sensor-icon"></div>
          <div className="sensor-label">Temperature</div>
          <div className="sensor-value">
            {sensorData.temperature !== null ? `${sensorData.temperature}°C` : 'No Data'}
          </div>
        </div>

        <div className="sensor-box humidity">
          <div className="sensor-icon"></div>
          <div className="sensor-label">Humidity</div>
          <div className="sensor-value">
            {sensorData.humidity !== null ? `${sensorData.humidity}%` : 'No Data'}
          </div>
        </div>

        <div className="sensor-box light">
          <div className="sensor-icon"></div>
          <div className="sensor-label">Light Level</div>
          <div className="sensor-value">
            {sensorData.light !== null ? sensorData.light : 'No Data'}
          </div>
        </div>

        <div className="sensor-box ultrasonic">
          <div className="sensor-icon"></div>
          <div className="sensor-label">Distance</div>
          <div className="sensor-value">
            {sensorData.ultrasonic !== null ? `${sensorData.ultrasonic} cm` : 'No Data'}
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

      {pictureStatus && (
        <div className="picture-status">
          {pictureStatus}
        </div>
      )}
    </div>
  );
}

export default App;
