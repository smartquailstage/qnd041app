import requests

def send_webhook_to_n8n(user_phone, user_name, desired_date):
    webhook_url = "https://tuservidor-n8n.com/webhook/agendar-cita"
    payload = {
        "name": user_name or "Cliente",
        "phone": user_phone,
        "date": desired_date,
        "event_title": "Cita con CTO Mauricio Silva - SmartQuail"
    }
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}
