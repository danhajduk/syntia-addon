import requests
from datetime import datetime, timedelta
from utils import log

USAGE_ENDPOINT = "https://api.openai.com/dashboard/billing/usage"

def get_usage(api_key, days=30):
    try:
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days)

        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }

        response = requests.get(USAGE_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        total_usage = data.get("total_usage", 0) / 100.0  # in USD
        return {
            "total_usage": round(total_usage, 4),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }

    except Exception as e:
        log(f"❌ Failed to get usage: {e}", "error")
        return {
            "total_usage": "Unavailable",
            "start_date": None,
            "end_date": None
        }
