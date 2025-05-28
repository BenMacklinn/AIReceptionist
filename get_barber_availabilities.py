import urllib.request
import json
from typing import Dict, Any, List
from get_barbers import get_barbers
from datetime import datetime

def get_barber_availabilities(barber_id: str, date: str) -> Dict[str, Any]:
    """
    Fetches (for a given barber and date) the schedule-time-range data (morning, afternoon, evening) and returns the availabilities.
    """
    url = f"https://api.getsquire.com/v1/barber/{barber_id}/schedule-time-range/{date}/{date}/30"
    req = urllib.request.Request(url)
    req.add_header('accept', '*/*')
    req.add_header('accept-language', 'en-GB,en-US;q=0.9,en;q=0.8')
    req.add_header('content-type', 'application/json')
    req.add_header('origin', 'https://getsquire.com')
    req.add_header('referer', 'https://getsquire.com/')
    req.add_header('squire-version', '2022-09-02')
    req.add_header('user-agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1')
    req.add_header('x-timezone', 'America/Toronto')
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode())
        if data and len(data) > 0:
            return data[0]  # Return the first (and only) day's data
        return {}
    except Exception as e:
        print(f"Error fetching availabilities for barber {barber_id} on {date}: {e}")
        return {}

def print_all_barbers_availabilities():
    barbers = get_barbers()
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"Today's date: {today}\n")
    for barber in barbers:
        name = barber.get('name', 'Unknown')
        barber_id = barber.get('id', '')
        avail = get_barber_availabilities(barber_id, today)
        print(f"{name} (ID: {barber_id}):")
        if not avail:
            print("  No availability data (or error).")
        else:
            times = avail.get("times", {})
            if times.get("morning"):
                print("  Morning: Available (times: " + ", ".join([t.get("time", "") for t in times["morning"] if t.get("available")]) + ")")
            else:
                print("  Morning: Not available")
            if times.get("afternoon"):
                print("  Afternoon: Available (times: " + ", ".join([t.get("time", "") for t in times["afternoon"] if t.get("available")]) + ")")
            else:
                print("  Afternoon: Not available")
            if times.get("evening"):
                print("  Evening: Available (times: " + ", ".join([t.get("time", "") for t in times["evening"] if t.get("available")]) + ")")
            else:
                print("  Evening: Not available")
        print()

if __name__ == "__main__":
    print_all_barbers_availabilities() 