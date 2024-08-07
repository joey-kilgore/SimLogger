from SimLogger import SimLogger
import requests

def sendNotification(text, endpoint):
    """Send notification using notify! Check the README.md for setup details.

    Args:
        text (str): text that will be sent as the notification (typically simTag and
            message) 
        endpoint (str): The channel the notifications will be sent to

    """

    endpoint = endpoint.replace("/c/","/").strip("/")

    SimLogger.logNotes(f"USING NOTIFY ENDPOINT: {endpoint}")
    response = requests.post(endpoint, data=text, headers={})
    SimLogger.logNotes(f"NOTIFICATION SENT:{str(response)} {text}")
