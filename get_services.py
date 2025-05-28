import urllib.request
import json
from typing import List, Dict, Any

def format_price(cents: int) -> str:
    return f"${cents/100:.2f}"

def get_services() -> List[Dict[str, Any]]:
    """
    Fetches service data from Squire API and prints a formatted list of available services.
    """
    print("Starting service data fetch...")
    url = "https://api.getsquire.com/v1/shop/f02998f1-d668-4443-9510-05053bafde9f/service"
    req = urllib.request.Request(url)
    req.add_header('accept', '*/*')
    req.add_header('accept-language', 'en-GB,en-US;q=0.9,en;q=0.8')
    req.add_header('content-type', 'application/json')
    req.add_header('origin', 'https://getsquire.com')
    req.add_header('referer', 'https://getsquire.com/')
    req.add_header('squire-version', '2022-09-02')
    req.add_header('user-agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1')
    req.add_header('x-timezone', 'America/Toronto')
    print(f"Making request to: {url}")
    try:
        print("Sending request...")
        response = urllib.request.urlopen(req)
        print(f"Response status code: {response.status}")
        data = json.loads(response.read().decode())
        print(f"Total services in response: {len(data)}")
        services = []
        seen_services = set()
        for service in data:
            if not isinstance(service, dict):
                continue
            name = service.get('name', '')
            if not name or not service.get('enabled', False) or name in seen_services:
                continue
            seen_services.add(name)
            tax_info = service.get('tax', {})
            if isinstance(tax_info, list):
                tax_info = tax_info[0] if tax_info else {}
            tax_percentage = tax_info.get('percentage', 0) if isinstance(tax_info, dict) else 0
            formatted_service = {
                "name": name,
                "duration": f"{service.get('duration', 0)} minutes",
                "price": format_price(service.get('cost', 0)),
                "price_with_tax": format_price(service.get('costWithTaxes', 0)),
                "tax_percentage": f"{tax_percentage}%",
                "requires_deposit": service.get('requiresDeposit', False),
                "kiosk_enabled": service.get('kioskEnabled', False),
                "description": service.get('desc', 'No description available')
            }
            services.append(formatted_service)
            print(f"Added service: {formatted_service['name']} - {formatted_service['price']} ({formatted_service['duration']})")
        services.sort(key=lambda x: float(x['price'].replace('$', '')))
        print(f"\nTotal available services found: {len(services)}")
        if services:
            print("\nFinal formatted service data:")
            print(json.dumps(services, indent=2))
        else:
            print("\nNo available services found.")
        return services
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
    get_services() 