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
const fetch = require('node-fetch');
const WebSocket = require('ws');

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

const ASSEMBLYAI_API_KEY = process.env.ASSEMBLYAI_API_KEY;
const ASSEMBLYAI_REALTIME_URL = 'wss://api.assemblyai.com/v2/realtime/ws?sample_rate=8000';

wss.on('connection', (ws) => {
  console.log('New WebSocket connection established');
  
  // Open a WebSocket connection to AssemblyAI for this call
  const aaiSocket = new WebSocket(ASSEMBLYAI_REALTIME_URL, {
    headers: { Authorization: ASSEMBLYAI_API_KEY }
  });

  aaiSocket.on('open', () => {
    console.log('Connected to AssemblyAI real-time API');
  });

  aaiSocket.on('message', (msg) => {
    const res = JSON.parse(msg);
    if (res.text && res.message_type === 'FinalTranscript') {
      // Pass the transcription to your AI logic
      handleTranscription({ callSid: 'twilio', transcription: res.text }, ws);
    }
  });

  aaiSocket.on('close', () => {
    console.log('AssemblyAI socket closed');
  });

  aaiSocket.on('error', (err) => {
    console.error('AssemblyAI socket error:', err);
  });

  ws.on('message', (message) => {
    // Only forward binary audio data to AssemblyAI
    if (typeof message !== 'string') {
      // Twilio sends audio as base64-encoded in JSON, so decode if needed
      // But in most cases, message is already a Buffer
      aaiSocket.readyState === WebSocket.OPEN && aaiSocket.send(message);
    } else {
      // Optionally handle Twilio JSON messages (e.g., stream_status)
      try {
        const data = JSON.parse(message);
        if (data.event === 'start') {
          console.log('Twilio stream started');
        } else if (data.event === 'stop') {
          console.log('Twilio stream stopped');
        }
      } catch (e) {
        // Ignore non-JSON or unrecognized messages
      }
    }
  });

  ws.on('close', () => {
    console.log('WebSocket connection closed');
    aaiSocket.close();
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