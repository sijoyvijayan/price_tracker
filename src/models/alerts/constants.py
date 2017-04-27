import os

URL = os.environ.get("MAILGUN_URL")
API_KEY = os.environ.get("MAILGUN_API_KEY")
FROM = os.environ.get("MAILGUN_FROM")
ALERT_TIMEOUT = 1
COLLECTION = "alerts"
FQDN = "pricing.jstlvr.com"
