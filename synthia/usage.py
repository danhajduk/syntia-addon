import requests
from datetime import datetime, timedelta
from utils import log

COSTS_URL = "https://api.openai.com/v1/organization/costs"

def get_costs(api_key, days=2):
    log("📊 Fetching cost data from OpenAI org endpoint", "debug")

    try:
        end_date = datetime.utcnow()
        start_date = (end_date - timedelta(days=days)).replace(hour=0, minute=0, second=0, microsecond=0)

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        params = {
            "start_time": int(start_date.timestamp()),
            "group_by": ["project_id"]
        }

        response = requests.get(COSTS_URL, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()

        total_cost = 0.0
        currency = "usd"

        for bucket in data.get("data", []):
            for result in bucket.get("results", []):
                amount = result.get("amount", {})
                value = amount.get("value", 0.0)
                currency = amount.get("currency", "usd")
                total_cost += value

        log(f"✅ Cost usage: {total_cost:.4f} {currency.upper()} over {days} days", "info")

        return {
            "total_cost": round(total_cost, 4),
            "currency": currency.upper(),
            "start_time": start_date.isoformat(),
            "end_time": end_date.isoformat()
        }

    except Exception as e:
        log(f"❌ Failed to fetch cost data: {e}", "error")
        return {
            "total_cost": "Unavailable",
            "currency": "USD",
            "start_time": None,
            "end_time": None
        }
