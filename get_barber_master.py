import json
from get_barbers import get_barbers
from get_barber_services import get_barber_services
from get_barber_availabilities import get_barber_availabilities
from datetime import datetime

def print_barber_master_summary():
    barbers = get_barbers()
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"Master Barber Summary (Today's date: {today})\n")
    for barber in barbers:
        name = barber.get("name", "Unknown")
        barber_id = barber.get("id", "")
        next_available = barber.get("next_available", "N/A")
        weekly_schedule = barber.get("weekly_schedule", {})
        services = get_barber_services(barber_id)  # (using today as start and end date)
        avail = get_barber_availabilities(barber_id, today)
        print("=" * 80)
        print(f" Barber: {name} (ID: {barber_id})")
        print("–" * 80)
        print(f" Next Available: {next_available}")
        print(" Weekly Schedule:")
        for (day, hours) in weekly_schedule.items():
            print(f"   {day}: {hours}")
        print(" Services:")
        if services:
            for svc in services:
                cost = svc.get('cost', None)
                if cost is not None:
                    price_str = f"${cost/100:.2f}"
                else:
                    price_str = "N/A"
                print(f"   – {svc.get('name', 'N/A')} (Duration: {svc.get('duration', 'N/A')} min, Price: {price_str})")
        else:
            print("   (No services returned.)")
        print(" Availabilities (Today):")
        if avail:
            times = avail.get("times", {})
            if times.get("morning"):
                print("   Morning: Available (times: " + ", ".join([t.get("time", "") for t in times["morning"] if t.get("available")]) + ")")
            else:
                print("   Morning: Not available")
            if times.get("afternoon"):
                print("   Afternoon: Available (times: " + ", ".join([t.get("time", "") for t in times["afternoon"] if t.get("available")]) + ")")
            else:
                print("   Afternoon: Not available")
            if times.get("evening"):
                print("   Evening: Available (times: " + ", ".join([t.get("time", "") for t in times["evening"] if t.get("available")]) + ")")
            else:
                print("   Evening: Not available")
        else:
            print("   (No availability data (or error).)")
        print("=" * 80 + "\n")

if __name__ == "__main__":
    print_barber_master_summary() 