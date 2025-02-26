import requests
import json

def send_fcm_notification(token, title, message):
    server_key = "YOUR_SERVER_KEY"
    url = "https://fcm.googleapis.com/fcm/send"

    headers = {
        "Authorization": f"key={server_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "to": token,
        "notification": {
            "title": title,
            "body": message,
            "click_action": "FLUTTER_NOTIFICATION_CLICK",
        },
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()
