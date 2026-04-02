import os
import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Variables Railway
GOOGLE_CLIENT_ID = os.getenv("CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

def get_access_token():
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }

    response = requests.post(url, data=data)
    token_data = response.json()

    if "access_token" not in token_data:
        print("Erreur Google:", token_data)
        raise Exception("Impossible d'obtenir un access_token")

    return token_data["access_token"]


@app.post("/create_event")
def create_event(event: dict):
    access_token = get_access_token()

    url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=event)

    if response.status_code not in [200, 201]:
        print("Erreur Google Calendar:", response.text)
        raise HTTPException(status_code=400, detail=response.json())

    return response.json()
