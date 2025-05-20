require('dotenv').config();
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const twilio = require('twilio');
const { WebSocketServer } = require('ws');
const http = require('http');
const { handleVoiceWebhook } = require('./routes/voice');
const { handleTranscription } = require('./routes/transcription');
const { handleBooking } = require('./routes/booking');

const app = express();
const port = process.env.PORT || 3000;

// Create HTTP server
const server = http.createServer(app);

// Initialize Twilio client
const twilioClient = twilio(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// WebSocket server for real-time communication
const wss = new WebSocketServer({ server });

wss.on('connection', (ws) => {
  console.log('New WebSocket connection established');
  
  ws.on('message', (message) => {
    // Check if the message is a string (likely JSON), otherwise it's binary/audio data
    if (typeof message === 'string') {
      try {
        const data = JSON.parse(message);
        // Handle different types of WebSocket messages
        switch (data.type) {
          case 'transcription':
            handleTranscription(data, ws);
            break;
          case 'stream_status':
            console.log('Stream status:', data.status);
            break;
          default:
            console.log('Unknown message type:', data.type);
        }
      } catch (error) {
        console.error('Error processing WebSocket JSON message:', error);
      }
    } else {
      // It's likely binary audio data from Twilio Media Streams
      // You can process the audio here if needed, or just ignore for now
      // console.log('Received binary audio data');
    }
  });

  ws.on('close', () => {
    console.log('WebSocket connection closed');
  });
});

// Routes
app.post('/voice', handleVoiceWebhook);
app.post('/transcription', handleTranscription);
app.post('/book-appointment', handleBooking);

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok' });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Something went wrong!',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined
  });
});

// Start server
server.listen(port, () => {
  console.log(`Server is running on port ${port}`);
}); 