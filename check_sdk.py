import os
import requests
from bs4 import BeautifulSoup

# URLs to monitor
SDK_URL = "https://live.zwidgets.com/js-sdk/1.5/ZohoEmbededAppSDK.min.js"
DOCS_URL = "https://www.zohocrm.dev/explore/widgets/v1.5/jssdk"

def send_alert(message):
    """Send alert via Slack Webhook (or replace with Discord/Email API)."""
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if webhook_url:
        requests.post(webhook_url, json={"text": message})
    else:
        print(f"ALERT: {message}")

def check_sdk_headers():
    """Checks HTTP HEAD request for CDN file modifications."""
    response = requests.head(SDK_URL)
    etag = response.headers.get("ETag")
    last_modified = response.headers.get("Last-Modified")
    print(f"Current ETag: {etag}")
    print(f"Last Modified: {last_modified}")
    # Compare against stored etag/last-modified value in your DB or repo state file

def check_next_version():
    """Proactively checks if a higher version endpoint (e.g. 1.6 or 2.0) exists."""
    possible_versions = ["1.6", "1.7", "2.0"]
    for version in possible_versions:
        test_url = f"https://live.zwidgets.com/js-sdk/{version}/ZohoEmbededAppSDK.min.js"
        res = requests.head(test_url)
        if res.status_code == 200:
            send_alert(f"🚨 New Zoho SDK Version Detected! Found active endpoint at: {test_url}")

if __name__ == "__main__":
    check_sdk_headers()
    check_next_version()
