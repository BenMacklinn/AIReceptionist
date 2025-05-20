const OpenAI = require('openai');
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// Store conversation state for each call
const callStates = new Map();

const extractBookingIntent = async (transcription) => {
  const prompt = `Extract booking information from the following text. Return a JSON object with these fields if present: name, service, date, time. If any field is not mentioned, set it to null. Text: "${transcription}"`;
  
  try {
    const completion = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        { role: "system", content: "You are a helpful assistant that extracts booking information from text. Return only valid JSON." },
        { role: "user", content: prompt }
      ],
      response_format: { type: "json_object" }
    });

    return JSON.parse(completion.choices[0].message.content);
  } catch (error) {
    console.error('Error extracting booking intent:', error);
    return null;
  }
};

const generateResponse = async (bookingInfo, callState) => {
  const missingFields = [];
  if (!bookingInfo.service) missingFields.push('service');
  if (!bookingInfo.date) missingFields.push('date');
  if (!bookingInfo.time) missingFields.push('time');

  if (missingFields.length === 0) {
    // All information is collected, confirm booking
    return {
      text: `Great! I've got all the information. You're booked for ${bookingInfo.service} on ${bookingInfo.date} at ${bookingInfo.time}. Would you like to receive a confirmation?`,
      complete: true
    };
  }

  // Ask for missing information
  const questions = {
    service: "What service would you like to book?",
    date: "What day would you like to book?",
    time: "What time would you like to book?"
  };

  return {
    text: questions[missingFields[0]],
    complete: false
  };
};

const handleTranscription = async (data, ws) => {
  const { callSid, transcription } = data;
  
  // Initialize or get call state
  if (!callStates.has(callSid)) {
    callStates.set(callSid, {
      bookingInfo: {},
      conversationHistory: []
    });
  }
  
  const callState = callStates.get(callSid);
  callState.conversationHistory.push({ role: 'user', content: transcription });

  // Extract booking intent
  const bookingInfo = await extractBookingIntent(transcription);
  if (bookingInfo) {
    // Update call state with new information
    callState.bookingInfo = {
      ...callState.bookingInfo,
      ...bookingInfo
    };
  }

  // Generate response
  const response = await generateResponse(callState.bookingInfo, callState);
  
  // Convert response to speech using OpenAI TTS
  try {
    const mp3 = await openai.audio.speech.create({
      model: "tts-1",
      voice: "alloy",
      input: response.text
    });

    // Send response back through WebSocket
    ws.send(JSON.stringify({
      type: 'response',
      text: response.text,
      audio: mp3,
      complete: response.complete
    }));

    // If booking is complete, trigger n8n webhook
    if (response.complete) {
      // TODO: Implement n8n webhook call
      callStates.delete(callSid); // Clean up call state
    }
  } catch (error) {
    console.error('Error generating speech:', error);
    ws.send(JSON.stringify({
      type: 'error',
      message: 'Sorry, I encountered an error. Please try again.'
    }));
  }
};

module.exports = {
  handleTranscription
}; 