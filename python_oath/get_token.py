import requests
import json
import os

def get_token():
    session = requests.Session()
    data = {
        "username": os.getenv('USERNAME'),
        "password": os.getenv('PASSWORD'),
        "grant_type": "password",
        "client_id": os.getenv('CLIENT_ID'),
        "scope": os.getenv('SCOPE'),
        "acr_values": os.getenv('ACR_VALUES')
    }
    response = session.post(os.getenv('TOKEN_ENDPOINT'), data=data)  # Use session.post instead of requests.post
    response.raise_for_status()
    return response.json()["access_token"]