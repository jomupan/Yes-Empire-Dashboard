import requests
from datetime import datetime, timezone

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

def get_stale_open_deals(api_key, location_id, days=30):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Version": "2021-07-28"
    }
    params = {"location_id": location_id, "status": "open"}
    res = requests.get(f"{BASE_URL}/opportunities/search", headers=headers, params=params)
    data = res.json()
    opportunities = data.get("opportunities", [])
    stale = 0
    now = datetime.now(timezone.utc)
    for opp in opportunities:
        created = opp.get("createdAt", "")
        if created:
            created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            diff = (now - created_dt).days
            if diff > days:
                stale += 1
    return stale