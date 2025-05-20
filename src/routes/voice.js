const twilio = require('twilio');
const VoiceResponse = twilio.twiml.VoiceResponse;

const handleVoiceWebhook = (req, res) => {
  const twiml = new VoiceResponse();
  
  // Greet the caller
  twiml.say({
    voice: 'Polly.Amy-Neural',
    language: 'en-GB'
  }, 'Welcome to our AI receptionist. How can I help you today?');

  // Start streaming the call audio
  const connect = twiml.connect();
  
  // Use the same host for WebSocket as the HTTP server
  const wsUrl = process.env.NODE_ENV === 'production'
    ? `wss://${req.headers.host}`
    : `ws://${req.headers.host}`;
    
  connect.stream({
    url: wsUrl,
    track: 'inbound_track'
  });

  // Send the TwiML response
  res.type('text/xml');
  res.send(twiml.toString());
};

module.exports = {
  handleVoiceWebhook
}; 