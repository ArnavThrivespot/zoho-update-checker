import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

# URLs to monitor
SDK_URL = "https://live.zwidgets.com/js-sdk/1.5/ZohoEmbededAppSDK.min.js"

def send_alert(message):
    """Send alert via Email using SMTP."""
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    recipient_email = os.environ.get("RECIPIENT_EMAIL")

    if not all([sender_email, sender_password, recipient_email]):
        print(f"EMAIL CONFIG MISSING. Alert text: {message}")
        return

    # Create Email Message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "🚨 Zoho SDK Version Change Detected!"
    
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure connection
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email alert sent successfully!")
    except Exception as e:
        print(f"Failed to send email alert: {e}")

def check_sdk_headers():
    """Checks HTTP HEAD request for CDN file modifications."""
    response = requests.head(SDK_URL)
    etag = response.headers.get("ETag")
    last_modified = response.headers.get("Last-Modified")
    print(f"Current ETag: {etag}")
    print(f"Last Modified: {last_modified}")

def check_next_version():
    """Proactively checks if a higher version endpoint (e.g. 1.6 or 2.0) exists."""
    possible_versions = ["1.6", "1.7", "2.0"]
    for version in possible_versions:
        test_url = f"https://live.zwidgets.com/js-sdk/{version}/ZohoEmbededAppSDK.min.js"
        res = requests.head(test_url)
        if res.status_code == 200:
            send_alert(f"New Zoho SDK Version Detected!\n\nFound active endpoint at: {test_url}")

if __name__ == "__main__":
    check_sdk_headers()
    check_next_version()
