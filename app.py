from flask import Flask, render_template
from dotenv import load_dotenv
from ghl_client import get_contacts, get_opportunities, get_stale_open_deals
import os
import datetime

load_dotenv()
app = Flask(__name__)

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

        try:
            won = opp_stats.get("won", 0)
            lost = opp_stats.get("lost", 0)
            closed = won + lost
            win_rate = round((won / closed) * 100, 1) if closed > 0 else None
        except:
            win_rate = None

        try:
            stale = get_stale_open_deals(key, loc)
        except:
            stale = "Error"

        data[name] = {
            "total_contacts": total_contacts,
            "opportunities": opp_stats,
            "win_rate": win_rate,
            "stale_deals": stale,
        }

    last_updated = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
    return render_template("dashboard.html", data=data, last_updated=last_updated)

if __name__ == "__main__":
    app.run(debug=True)
