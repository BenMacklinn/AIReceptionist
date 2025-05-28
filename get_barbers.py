import urllib.request
import json
from typing import List, Dict, Any

WEEKDAYS = [
    None, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]

def format_time(hour: int, minute: int) -> str:
    return f"{hour:02}:{minute:02}"

def get_barbers() -> List[Dict[str, Any]]:
    """
    Fetches barber data from Squire API and returns list of barbers with their schedules.
    """
    url = "https://api.getsquire.com/v1/shop/ultimate-fades-avenue-toronto/professional?include=photos,days_on,days_off,reward,schedules&sortBy=order:asc,createdAt:desc"
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
        barbers = []
        for item in data:
            barber = item.get('barber', {})
            next_available = item.get('nextAvailableTimeText', '')
            barber_id = barber.get('id', '')
            formatted_barber = {
                "name": f"{barber.get('firstName', '')} {barber.get('lastName', '')}".strip(),
                "id": barber_id,
                "next_available": next_available,
                "schedule": [
                    {
                        "day": WEEKDAYS[workday.get("weekDay")] if 1 <= workday.get("weekDay") <= 7 else str(workday.get("weekDay")),
                        "enabled": workday.get("enabled", False),
                        "start": format_time(workday.get("startHour", 0), workday.get("startMinute", 0)) if workday.get("enabled") else None,
                        "end": format_time(workday.get("finishHour", 0), workday.get("finishMinute", 0)) if workday.get("enabled") else None
                    }
                    for schedule in barber.get("schedules", [])
                    for workday in schedule.get("workdays", [])
                ]
            }
            barbers.append(formatted_barber)
        return barbers
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        print(f"Response: {e.read().decode()}")
        return []
    except urllib.error.URLError as e:
        print(f"URL Error: {str(e)}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON Error: {str(e)}")
        return []
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return []

if __name__ == "__main__":
    barbers = get_barbers()
    for barber in barbers:
        print(f"Barber: {barber['name']} (ID: {barber['id']})")
        print(f"  Next available: {barber['next_available']}")
        print("  Weekly Schedule:")
        for day in barber['schedule']:
            day_name = day['day']
            if day['enabled']:
                print(f"    {day_name}: {day['start']} - {day['end']}")
            else:
                print(f"    {day_name}: Closed")
        print()
    print("\nScript completed.") 