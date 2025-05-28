import urllib.request
import json
from typing import List, Dict, Any
from get_barbers import get_barbers

def get_barber_services(barber_id: str) -> List[Dict[str, Any]]:
    """
    Fetches services offered by a specific barber using the v2 endpoint.
    """
    shop_id = "f02998f1-d668-4443-9510-05053bafde9f"
    url = f"https://api.getsquire.com/v2/shop/{shop_id}/barber/{barber_id}/service?sortBy=order&include=addonServices&limit=500"
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
        services = json.loads(response.read().decode())
        return services
    except Exception:
        return []

def print_all_barbers_services():
    barbers = get_barbers()
    for barber in barbers:
        name = barber.get('name', 'Unknown')
        barber_id = barber.get('id', '')
        print(f"{name}:")
        services = get_barber_services(barber_id)
        if not services:
            print("  No services found.")
            continue
        for service in services:
            if service.get('enabled', True):
                sname = service.get('name', 'Unknown')
                duration = service.get('duration', 0)
                price = service.get('cost', 0) / 100
                desc = service.get('desc', '')
                line = f"  - {sname} ({duration} min, ${price:.2f})"
                if desc:
                    line += f" - {desc}"
                print(line)
        print()

if __name__ == "__main__":
    print_all_barbers_services() 