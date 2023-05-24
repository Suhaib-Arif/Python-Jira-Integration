import os
import requests
import logging
from twilio.rest import Client
from flask import Flask, request

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get environment variables
token = os.environ.get("TOKEN")
account_id = os.environ.get("ACCOUNT_ID")
auth_token = os.environ.get("AUTH_TOKEN")
project_key = os.environ.get("PROJECT_KEY")
jira_token = os.environ.get("JIRA_TOKEN")
email = os.environ.get("EMAIL")
url = os.environ.get("URL")

client = Client(account_id, auth_token)

def create_issue(message):
    issue_data = {
        "fields": {
            "project": {
                "key": project_key,
            },
            "summary": message,
            "description": message,
            "issuetype": {
                "name": "Task"
            }
        }
    }

    session = requests.Session()
    session.auth = (email, jira_token)

    try:
        response = session.post(url, json=issue_data)
        response.raise_for_status()  # Raise an exception for non-2xx response codes
        return response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error creating Jira issue: %s", str(e))
        return None


@app.route("/")
def home():
    return "Home"

@app.route("/whatsapp", methods=["POST"])
def message():
    try:
        data = request.form
        message = data.get("Body")
        logger.info("Received message: %s", message)
        create_issue(message)
        return "Waiting..."
    except Exception as e:
        logger.error("Error processing WhatsApp message: %s", str(e))
        return "Error"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
