const axios = require('axios');

const handleBooking = async (req, res) => {
  const { bookingInfo, callSid, phoneNumber } = req.body;

  if (!bookingInfo || !callSid || !phoneNumber) {
    return res.status(400).json({
      error: 'Missing required booking information'
    });
  }

  try {
    // Send booking information to n8n webhook
    const response = await axios.post(process.env.N8N_WEBHOOK_URL, {
      bookingInfo,
      callSid,
      phoneNumber,
      timestamp: new Date().toISOString()
    });

    res.status(200).json({
      success: true,
      message: 'Booking information sent to n8n',
      n8nResponse: response.data
    });
  } catch (error) {
    console.error('Error sending booking to n8n:', error);
    res.status(500).json({
      error: 'Failed to process booking',
      message: error.message
    });
  }
};

module.exports = {
  handleBooking
}; 