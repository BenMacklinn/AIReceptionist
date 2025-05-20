# AI Receptionist

An intelligent receptionist system that handles incoming calls, processes speech, and books appointments automatically using Twilio, OpenAI, and n8n.

## Features

- Automated call handling with Twilio
- Real-time speech-to-text transcription
- Natural language processing for booking intent
- Text-to-speech responses using OpenAI
- Integration with n8n for appointment booking
- WebSocket support for real-time communication

## Prerequisites

- Node.js (v14 or higher)
- Twilio account with a phone number
- OpenAI API key
- n8n instance with webhook endpoint

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number_here

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Server Configuration
PORT=3000
N8N_WEBHOOK_URL=your_n8n_webhook_url_here
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create and configure your `.env` file
4. Start the development server:
   ```bash
   npm run dev
   ```

## Twilio Configuration

1. Log in to your Twilio Console
2. Go to Phone Numbers > Manage > Active Numbers
3. Select your phone number
4. Under "Voice & Fax" > "A Call Comes In", set the webhook URL to:
   ```
   https://your-domain.com/voice
   ```
5. Make sure to use HTTP POST as the method

## API Endpoints

- `POST /voice` - Twilio webhook for incoming calls
- `POST /transcription` - Handles speech transcription
- `POST /book-appointment` - Sends booking information to n8n
- `GET /health` - Health check endpoint

## WebSocket Events

The server uses WebSocket for real-time communication:

- `transcription` - Receives transcribed speech
- `stream_status` - Updates about the audio stream status
- `response` - Sends AI responses back to the client

## Development

- `npm run dev` - Start development server with hot reload
- `npm start` - Start production server
- `npm test` - Run tests

## Security Considerations

- Keep your `.env` file secure and never commit it to version control
- Use HTTPS in production
- Implement rate limiting for production use
- Validate all incoming webhook requests from Twilio

## License

MIT 