require('dotenv').config();
const fs = require('fs');
const cors = require("cors");
const express = require("express");
const http = require('http');
const MQTT = require('mqtt');
const { spawn } = require('child_process');
const APP = express();
const server = http.createServer(APP);
const { Server } = require("socket.io");

const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

const CLIENTID = "backend_" + Math.random().toString(16).substr(2, 8);

console.log(`Connecting to MQTT with client ID: ${CLIENTID}`);
console.log(`MQTT URL: ${process.env.CONNECT_URL}`);
console.log(`MQTT User: ${process.env.MQTT_USER}`);

const client = MQTT.connect(process.env.CONNECT_URL, {
  clientId: CLIENTID,
  clean: true,
  connectTimeout: 15000,
  username: process.env.MQTT_USER,
  password: process.env.MQTT_PASS,
  reconnectPeriod: 5000,
  keepalive: 60,
  rejectUnauthorized: false,
  protocolVersion: 4
});

// Used for debugging 

client.on("error", function (error) {
  console.error("Connection error: ", error);
});

client.on("close", function () {
  console.log("Connection closed");
});

client.on("offline", function () {
  console.log("Client went offline");
});

client.on("reconnect", function () {
  console.log("Attempting to reconnect...");
});

// MQTT Connection

client.on('connect', async () => {
  console.log("Connected");

  client.subscribe("ultrasonic", (err) => {
    if (err) {
      console.error("Subscription error for 'ultrasonic': ", err);
    } else {
      console.log("Subscribed to 'ultrasonic'");
    }
  });

  client.subscribe("temp", (err) => {
    if (err) {
      console.error("Subscription error for 'temp': ", err);
    } else {
      console.log("Subscribed to 'temp'");
    }
  });

  client.subscribe("humidity", (err) => {
    if (err) {
      console.error("Subscription error for 'temp': ", err);
    } else {
      console.log("Subscribed to 'humidity'");
    }
  });

  client.subscribe("light", (err) => {
    if (err) {
      console.error("Subscription error for 'light': ", err);
    } else {
      console.log("Subscribed to 'light'");
    }
  });
});


const corsOptions = {
  origin: '*'
};

APP.use(cors(corsOptions));
APP.use(express.json());

// Readings from sensors 
let latestTemp = null;
let latestUltrasonic = null;
let latestHumidity = null;
let latestLight = null;

io.on("connection", (socket) => {
  console.log("Frontend connected to socket");

  // Send the latest sensor data to the newly connected client
  if (latestTemp) {
    socket.emit('temp', latestTemp);
  }
  if (latestUltrasonic) socket.emit('ultrasonic', latestUltrasonic);
  if (latestLight) {
    socket.emit('light', latestLight);
  }

  // Listen for messages from the frontend
  socket.on('display', (message) => {
    console.log('🔥 Received message from frontend:', message);
    console.log('📡 Publishing to MQTT topic "display"...');
    
    const result = client.publish("display", message.toString());
    console.log('📤 MQTT publish result:', result);
    console.log('✅ Message sent to MQTT successfully');
  });

  // Handle take picture request
  socket.on('take_picture', () => {
    console.log('📸 Taking picture and getting AI description...');
    
    // Execute the Python script with full path
    const pythonProcess = spawn('C:/Users/dvoce/AppData/Local/Programs/Python/Python313/python.exe', ['../AI/receive.py', 'get_description'], {
      cwd: __dirname
    });

    let outputData = '';
    let errorData = '';

    pythonProcess.stdout.on('data', (data) => {
      outputData += data.toString();
      console.log(`Python output: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
      errorData += data.toString();
      console.error(`Python error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
      console.log(`Python script finished with code ${code}`);
      if (code === 0) {
        // Extract AI description from output
        let aiDescription = null;
        const startMarker = 'AI_DESCRIPTION_START';
        const endMarker = 'AI_DESCRIPTION_END';
        
        if (outputData.includes(startMarker) && outputData.includes(endMarker)) {
          const startIndex = outputData.indexOf(startMarker) + startMarker.length;
          const endIndex = outputData.indexOf(endMarker);
          aiDescription = outputData.substring(startIndex, endIndex).trim();
        }
        
        socket.emit('picture_taken', { 
          success: true, 
          message: 'Picture analyzed successfully!',
          description: aiDescription || 'Analysis completed but no description found',
          output: outputData
        });
      } else {
        socket.emit('picture_taken', { 
          success: false, 
          message: 'Failed to analyze picture',
          error: errorData
        });
      }
    });
  });

  socket.on("disconnect", () => {
    console.log("Frontend disconnected from socket");
  });

});

// Send latest readings to frontend every 500ms for real-time updates
setInterval(() => {
  io.emit('temp', latestTemp);
  io.emit('ultrasonic', latestUltrasonic);
  io.emit('humidity', latestHumidity);
  io.emit('light', latestLight)
}, 500);  // 500ms = twice per second for responsive UI

server.listen(8000, () => {
  console.log('Server is running on port 8000');
});

client.on('message', (TOPIC, payload) => {
  console.log("Received from broker:", TOPIC, payload.toString());
  
  // Always update to the latest value immediately
  if( TOPIC === 'temp' ) {
    latestTemp = payload.toString();
    console.log(`📊 Updated temperature: ${latestTemp}°C`);
  }
  else if ( TOPIC === 'ultrasonic' ) {
    latestUltrasonic = payload.toString();
    console.log(`📊 Updated distance: ${latestUltrasonic}cm`);
  }
  else if ( TOPIC === 'humidity') {
    latestHumidity = payload.toString();
    console.log(`📊 Updated humidity: ${latestHumidity}%`);
  }
  else if ( TOPIC === 'light') {
    latestLight = payload.toString();
    console.log(`📊 Updated light: ${latestLight}`);
  }
  
  // Immediately send the latest reading to all connected clients
  io.emit(TOPIC, payload.toString());
});

