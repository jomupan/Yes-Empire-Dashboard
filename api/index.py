from flask import Flask, render_template
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from ghl_client import get_contacts, get_opportunities

load_dotenv()
app = Flask(__name__, template_folder="../templates")

SUB_ACCOUNTS = {
    "YES Empire": {
        "api_key": os.getenv("YESEMPIRE_API_KEY"),
        "location_id": os.getenv("YESEMPIRE_LOCATION_ID"),
    },
    "Benashield": {
        "api_key": os.getenv("BENASHIELD_API_KEY"),
        "location_id": os.getenv("BENASHIELD_LOCATION_ID"),
    },
    "Benahous": {
        "api_key": os.getenv("BENAHOUS_API_KEY"),
        "location_id": os.getenv("BENAHOUS_LOCATION_ID"),
    },
    "Benaccount": {
        "api_key": os.getenv("BENACCOUNT_API_KEY"),
        "location_id": os.getenv("BENACCOUNT_LOCATION_ID"),
    },
}

@app.route("/")
def dashboard():
    data = {}
    for name, config in SUB_ACCOUNTS.items():
        key = config["api_key"]
        loc = config["location_id"]

        try:
            contacts = get_contacts(key, loc)
            total_contacts = contacts.get("meta", {}).get("total", 0)
        except:
            total_contacts = "Error"

        opp_stats = {}
        for status in ["open", "won", "lost", "abandoned"]:
            try:
                res = get_opportunities(key, loc, status=status)
                opp_stats[status] = res.get("meta", {}).get("total", 0)
            except:
                opp_stats[status] = "Error"

        opp_stats["total"] = sum(
            v for v in opp_stats.values() if isinstance(v, int)
        )

        data[name] = {
            "total_contacts": total_contacts,
            "opportunities": opp_stats,
        }

    return render_template("dashboard.html", data=data)
