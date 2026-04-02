from flask import Flask, request, redirect
import requests
import urllib.parse
import os

app = Flask(__name__)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# 1) Lancer l'auth Google
@app.route("/auth")
def auth():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/calendar.events",
        "access_type": "offline",
        "prompt": "consent"
    }
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)
    return redirect(url)

# 2) Callback OAuth → récupère access_token + refresh_token
@app.route("/oauth2callback")
def callback():
    code = request.args.get("code")
    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    r = requests.post(token_url, data=data)
    return r.json()

# 3) Endpoint pour créer un événement Google Calendar
@app.route("/create_event", methods=["POST"])
def create_event():
    access_token = request.json.get("access_token")

    event = {
        "summary": request.json.get("summary"),
        "start": {
            "dateTime": request.json.get("start"),
            "timeZone": "Europe/Brussels"
        },
        "end": {
            "dateTime": request.json.get("end"),
            "timeZone": "Europe/Brussels"
        }
    }

    r = requests.post(
        "https://www.googleapis.com/calendar/v3/calendars/primary/events",
        headers={"Authorization": f"Bearer {access_token}"},
        json=event
    )

    return r.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
