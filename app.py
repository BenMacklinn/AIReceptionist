from flask import Flask, jsonify, request
from get_barber_master import print_barber_master_summary
from get_barber_services import get_barber_services
from get_barber_availabilities import get_barber_availabilities
from get_barbers import get_barbers
from datetime import datetime, timezone, timedelta
import pytz
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "online", "message": "Barber Booking API is running"})

@app.route('/barbers', methods=['GET'])
def get_barbers_route():
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

# Helper functions

def filter_bookable_slots(avail_data, now):
    slots = {'morning': [], 'afternoon': [], 'evening': []}
    for period in ['morning', 'afternoon', 'evening']:
        for slot in avail_data.get('times', {}).get(period, []):
            if slot.get('available'):
                slot_time = datetime.fromisoformat(slot['time'].replace('Z', '+00:00'))
                if slot_time > now:
                    slots[period].append(slot['time'])
    return slots

def format_time_local(iso_time, tz_str='America/Toronto'):
    dt = datetime.fromisoformat(iso_time.replace('Z', '+00:00'))
    local_tz = pytz.timezone(tz_str)
    local_dt = dt.astimezone(local_tz)
    return local_dt.strftime('%-I:%M %p')

@app.route('/barber-summary', methods=['GET'])
def barber_summary():
    print("DEBUG: Returning availabilities for 2 days only")
    barbers = get_barbers()
    today = datetime.now(timezone.utc).date()
    now = datetime.now(timezone.utc)
    summary = []
    for barber in barbers:
        barber_id = barber.get('id', '')
        name = barber.get('name', 'Unknown')
        next_available = barber.get('next_available', 'N/A')
        weekly_schedule = barber.get('weekly_schedule', {}) if 'weekly_schedule' in barber else barber.get('schedule', {})
        services = get_barber_services(barber_id)
        # Format services for JSON
        formatted_services = [
            {
                'name': s.get('name', 'Unknown'),
                'duration': s.get('duration', 0),
                'price': s.get('cost', 0) / 100
            } for s in services
        ]
        # Availabilities for today and tomorrow only
        availabilities = {}
        for i in range(2):
            day_date = today + timedelta(days=i)
            day_str = day_date.strftime('%Y-%m-%d')
            avail = get_barber_availabilities(barber_id, day_str)
            filtered_avail = filter_bookable_slots(avail, now) if avail else {'morning': [], 'afternoon': [], 'evening': []}
            # Format times as human-readable
            formatted = {
                period: [format_time_local(t) for t in filtered_avail.get(period, [])]
                for period in ['morning', 'afternoon', 'evening']
            }
            availabilities[day_str] = formatted
        summary.append({
            'name': name,
            'id': barber_id,
            'next_available': next_available,
            'weekly_schedule': weekly_schedule,
            'services': formatted_services,
            'availabilities': availabilities
        })
    return jsonify(summary)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 