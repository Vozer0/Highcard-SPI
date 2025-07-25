import React, { useState, useEffect } from "react";
import io from 'socket.io-client';
import './App.css';

const socket = io('http://localhost:8000');

function App() {
  const [pictureStatus, setPictureStatus] = useState("");
  const [displayText, setDisplayText] = useState("");
  const [sendStatus, setSendStatus] = useState("");

  useEffect(() => {
    socket.on('connect', () => console.log('Connected:', socket.id));
    socket.on('picture_taken', data => {
      setPictureStatus(data.message);
      setTimeout(() => setPictureStatus(""), 3000); // Clear status after 3 seconds
    });
    return () => {
      socket.off('picture_taken');
    };
  }, []);

  const handleSendText = () => {
    if (displayText.trim()) {
      socket.emit('display', displayText);
      setSendStatus("Text sent to OLED!");
      setTimeout(() => setSendStatus(""), 2000); // Clear status after 2 seconds
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
            maxLength={100} // Limit text length for OLED display
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
