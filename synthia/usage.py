import requests
from datetime import datetime, timedelta
from utils import log

USAGE_ENDPOINT = "https://api.openai.com/v1/usage"

def get_usage(api_key, days=30):
    log(f"📡 Attempting to fetch usage data for the last {days} days...", "debug")

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

        log(f"📤 Requesting usage from {USAGE_ENDPOINT} with params {params}", "debug")
        response = requests.get(USAGE_ENDPOINT, headers=headers, params=params)

        if response.status_code == 403:
            log("🚫 403 Forbidden – API key lacks access to usage endpoint.", "error")
        elif response.status_code == 404:
            log("❓ 404 Not Found – API endpoint may be incorrect or deprecated.", "error")
        elif response.status_code != 200:
            log(f"❌ Unexpected status code: {response.status_code} — {response.text}", "error")

        response.raise_for_status()
        data = response.json()

        if "data" not in data:
            log(f"⚠️ Unexpected response format: {data}", "warning")
            return {
                "total_tokens": "Unavailable",
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }

        total_tokens = sum(item.get("n_tokens_total", 0) for item in data.get("data", []))

        log(f"✅ Usage fetched successfully: {total_tokens} tokens from {start_date} to {end_date}", "info")

        return {
            "total_tokens": total_tokens,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }

    except requests.exceptions.RequestException as e:
        log(f"❌ Network or HTTP error occurred: {e}", "error")
    except Exception as e:
        log(f"❌ Unexpected error in get_usage: {e}", "error")

    return {
        "total_tokens": "Unavailable",
        "start_date": None,
        "end_date": None
    }
