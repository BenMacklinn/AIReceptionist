from flask import Flask, jsonify, request
from get_barber_master import print_barber_master_summary
from get_barber_services import get_barber_services
from get_barber_availabilities import get_barber_availabilities
import json
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "online", "message": "Barber Booking API is running"})

@app.route('/barbers', methods=['GET'])
def get_barbers():
    try:
        # Get all barber data
        barbers_data = print_barber_master_summary()
        return jsonify({"status": "success", "data": barbers_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/barber/<barber_id>/services', methods=['GET'])
def barber_services(barber_id):
    try:
        services = get_barber_services(barber_id)
        return jsonify({"status": "success", "data": services})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/barber/<barber_id>/availability', methods=['GET'])
def barber_availability(barber_id):
    try:
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        availability = get_barber_availabilities(barber_id, date)
        return jsonify({"status": "success", "data": availability})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/check-booking', methods=['POST'])
def check_booking():
    try:
        data = request.json
        required_fields = ['barberId', 'dateTime', 'serviceId']
        
        # Check if all required fields are present
        if not all(field in data for field in required_fields):
            return jsonify({
                "status": "error",
                "message": "Missing required fields",
                "required": required_fields
            }), 400

        # Here you would add logic to:
        # 1. Check if the barber is available at that time
        # 2. Verify the service exists
        # 3. Format the booking payload
        
        # For now, we'll just return a mock response
        booking_payload = {
            "barberId": data['barberId'],
            "dateTime": data['dateTime'],
            "services": [{"id": data['serviceId']}],
            "tipPercentage": 25
        }

        return jsonify({
            "status": "success",
            "message": "Booking check successful",
            "payload": booking_payload
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 