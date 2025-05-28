import json
from get_barbers import get_barbers
from get_barber_services import get_barber_services
from get_barber_availabilities import get_barber_availabilities
from datetime import datetime

def print_barber_master_summary():
    barbers = get_barbers()
    today = datetime.now().strftime("%Y-%m-%d")
    all_barber_data = []
    for barber in barbers:
        name = barber.get("name", "Unknown")
        barber_id = barber.get("id", "")
        next_available = barber.get("next_available", "N/A")
        weekly_schedule = barber.get("weekly_schedule", {}) if "weekly_schedule" in barber else barber.get("schedule", {})
        services = get_barber_services(barber_id)
        avail = get_barber_availabilities(barber_id, today)
        barber_data = {
            "name": name,
            "id": barber_id,
            "next_available": next_available,
            "weekly_schedule": weekly_schedule,
            "services": services,
            "today_availability": avail
        }
        all_barber_data.append(barber_data)
    return all_barber_data

if __name__ == "__main__":
    # For CLI usage, print the summary
    data = print_barber_master_summary()
    print(json.dumps(data, indent=2)) 