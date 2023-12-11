import sys
sys.path.append("/home/neo/Documents/Projects/nodenomads_random_meets_api")

import os
import requests
import jwt
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from pydantic import BaseModel
from typing import Optional
from app.utils.constants import ZoomConfig
from datetime import datetime, timezone, timedelta
from config.supabase import supabase

load_dotenv()

account_id: str = os.environ.get("ZOOM_ACCOUNT_ID")
client_id: str = os.environ.get("ZOOM_CLIENT_ID")
secret_key: str = os.environ.get("ZOOM_CLIENT_SECRET")

def generate_access_token():
    auth = HTTPBasicAuth(client_id, secret_key)
    data = {
        "grant_type": "account_credentials",
        "account_id": account_id
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(
        ZoomConfig.ZOOM_OAUTH_ENDPOINT,
        auth=auth,
        data=data,
        headers=headers
    )

    response.raise_for_status()
    token_data = response.json()

    expires_in = token_data["expires_in"]
    access_token = token_data["access_token"]

    data, count = supabase.table('zoom_token').update({"jwt_token": access_token, "expires_in": expires_in}).eq("id", 1).execute()

    return access_token


def get_access_token():
    data, count = supabase.table('zoom_token').select("jwt_token", "expires_in").eq('id', 1).execute()
    token = data[1][0]["jwt_token"]
    expires_in = data[1][0]["expires_in"]
    try:
        current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
        expiration_time = current_time + timedelta(seconds=expires_in)
        if current_time > expiration_time:
            token = generate_access_token()
            return token
        else:
            return token
    
    except jwt.ExpiredSignatureError:
        # Token has already expired
        print("TOKEN ALREADY EXPIRED")

    except jwt.InvalidTokenError:
        # Token is invalid
        print("INVALID TOKEN")



if __name__ == "__main__":
    try:
        print(get_access_token())
    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")