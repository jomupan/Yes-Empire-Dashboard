import requests

BASE_URL = "https://services.leadconnectorhq.com"

def get_contacts(api_key, location_id):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Version": "2021-07-28"
    }
    params = {"locationId": location_id}
    res = requests.get(f"{BASE_URL}/contacts/", headers=headers, params=params)
    return res.json()

def get_opportunities(api_key, location_id, status=None):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Version": "2021-07-28"
    }
    params = {"location_id": location_id}
    if status:
        params["status"] = status
    res = requests.get(f"{BASE_URL}/opportunities/search", headers=headers, params=params)
    return res.json()