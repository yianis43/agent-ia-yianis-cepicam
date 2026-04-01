from flask import Flask, request
import requests

app = Flask(__name__)

CAL_API_KEY = "cal_live_c3cf5c23f7fbb2d821357daff52c448c"
EVENT_TYPE_ID = 5222644

CAL_API_URL = "https://api.cal.com/v1/bookings"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    nom = data.get("nom")
    email = data.get("email")
    date = data.get("date")
    heure = data.get("heure")

    if not all([nom, email, date, heure]):
        return {"error": "Missing required fields"}, 400

    start = f"{date}T{heure}:00Z"

    payload = {
        "eventTypeId": EVENT_TYPE_ID,
        "start": start,
        "name": nom,
        "email": email,
        "notes": "Rendez-vous créé automatiquement par l’agent IA Yianis"
    }

    headers = {
        "Authorization": f"Bearer {CAL_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(CAL_API_URL, json=payload, headers=headers)

    return {
        "status": "ok",
        "cal_response": response.json()
    }

if __name__ == "__main__":
    app.run(port=5000)
