import requests
from datetime import datetime, timedelta
from utils import log

USAGE_ENDPOINT = "https://api.openai.com/v1/usage"

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

        # Sum up token usage from daily entries
        total_tokens = sum(item.get("n_tokens_total", 0) for item in data.get("data", []))

        return {
            "total_tokens": total_tokens,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }

    except Exception as e:
        log(f"❌ Failed to get usage: {e}", "error")
        return {
            "total_tokens": "Unavailable",
            "start_date": None,
            "end_date": None
        }
