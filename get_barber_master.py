import json
from get_barbers import get_barbers
from get_barber_services import get_barber_services
from get_barber_availabilities import get_barber_availabilities
from datetime import datetime, timezone, timedelta
import pytz

def filter_bookable_slots(avail_data):
    slots = {'morning': [], 'afternoon': [], 'evening': []}
    now = datetime.now(timezone.utc)
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

def print_barber_master_summary():
    barbers = get_barbers()
    today = datetime.now().date()
    print(f"Master Barber Summary (Week starting: {today})\n")
    for barber in barbers:
        name = barber.get("name", "Unknown")
        barber_id = barber.get("id", "")
        next_available = barber.get("next_available", "N/A")
        weekly_schedule = barber.get("weekly_schedule", {}) if "weekly_schedule" in barber else barber.get("schedule", {})
        services = get_barber_services(barber_id)
        print("="*80)
        print(f" Barber: {name} (ID: {barber_id})")
        print("\u2014"*40)
        print(f" Next Available: {next_available}")
        print(" Weekly Schedule:")
        for day in weekly_schedule:
            day_name = day.get('day', '')
            enabled = day.get('enabled', False)
            start = day.get('start')
            end = day.get('end')
            if enabled:
                print(f"   {day_name}: {start} - {end}")
            else:
                print(f"   {day_name}: Closed")
        print(" Services:")
        for s in services:
            sname = s.get('name', 'Unknown')
            duration = s.get('duration', 0)
            price = s.get('cost', 0) / 100
            print(f"    {sname} (Duration: {duration} min, Price: ${price:.2f})")
        print(" Availabilities (Next 7 days):")
        for i in range(7):
            day_date = today + timedelta(days=i)
            day_str = day_date.strftime('%Y-%m-%d')
            day_label = day_date.strftime('%A, %b %d')
            avail = get_barber_availabilities(barber_id, day_str)
            filtered_avail = filter_bookable_slots(avail) if avail else {}
            print(f"  {day_label}:")
            for period in ['morning', 'afternoon', 'evening']:
                times = filtered_avail.get(period, [])
                if not times:
                    print(f"    {period.capitalize()}: Not available")
                else:
                    formatted_times = ', '.join([format_time_local(t) for t in times])
                    print(f"    {period.capitalize()}: Available (times: {formatted_times})")
        print("="*80 + "\n")

if __name__ == "__main__":
    print_barber_master_summary() 