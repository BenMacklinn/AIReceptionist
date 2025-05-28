# Barber Booking API

A Flask-based API for managing barber shop bookings, built to run on Render's free tier.

## API Endpoints

- `GET /`: Health check
- `GET /barbers`: Get all barbers and their details
- `GET /barber/<barber_id>/services`: Get services for a specific barber
- `GET /barber/<barber_id>/availability`: Get availability for a specific barber
- `POST /check-booking`: Check and format a booking request

## Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python app.py
```

## Deployment on Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Use the following settings:
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Python Version: 3.9.0

## Environment Variables

- `PORT`: The port the server runs on (default: 8080)

## API Usage Examples

### Check Barber Availability
```bash
curl "http://localhost:8080/barber/1a4e478b-80b3-4bca-8d6a-84f4caf6bd75/availability?date=2025-05-29"
```

### Check Booking
```bash
curl -X POST http://localhost:8080/check-booking \
  -H "Content-Type: application/json" \
  -d '{
    "barberId": "1a4e478b-80b3-4bca-8d6a-84f4caf6bd75",
    "dateTime": "2025-05-29T10:15:00-04:00",
    "serviceId": "4ae098c5-2bea-4314-b776-fdfb90437e4d"
  }'
``` 