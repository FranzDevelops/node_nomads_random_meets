import sys
import os
import jwt
import asyncio
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from pydantic import BaseModel
from typing import Optional
from app.utils.constants import ZoomConfig
from config.supabase import supabase
import aiohttp

load_dotenv()

account_id: str = os.environ.get("ZOOM_ACCOUNT_ID")
client_id: str = os.environ.get("ZOOM_CLIENT_ID")
secret_key: str = os.environ.get("ZOOM_CLIENT_SECRET")

async def generate_access_token():
    auth = HTTPBasicAuth(client_id, secret_key)
    data = {
        "grant_type": "account_credentials",
        "account_id": account_id
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with aiohttp.ClientSession() as session:
        async with session.post(
                ZoomConfig.ZOOM_OAUTH_ENDPOINT,
                auth=auth,
                data=data,
                headers=headers
        ) as response:
            response.raise_for_status()
            token_data = await response.json()

    expires_in = token_data["expires_in"]
    access_token = token_data["access_token"]

    current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    expiration_time = current_time + timedelta(seconds=expires_in)

    # Convert expiration_time to a string in a specific format
    expiration_time_str = expiration_time.strftime('%Y-%m-%d %H:%M:%S %Z')

    data, count = await supabase.table('zoom_token').update({"jwt_token": access_token, "expiration_time": expiration_time_str}).eq("id", 1).execute()

    return access_token

async def get_access_token():
    data, count = await supabase.table('zoom_token').select("jwt_token", "expiration_time").eq('id', 1).execute()
    token = data[1][0]["jwt_token"]
    expiration_time_str = data[1][0]["expiration_time"]
    expiration_time = datetime.strptime(expiration_time_str, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc)
    
    try:
        current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
        if current_time > expiration_time:
            token = await generate_access_token()
            return token
        else:
            return token
    except jwt.ExpiredSignatureError:
        # Token has already expired
        print("TOKEN ALREADY EXPIRED")
    except jwt.InvalidTokenError:
        # Token is invalid
        print("INVALID TOKEN")

async def main():
    try:
        print(await get_access_token())
    except aiohttp.ClientError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
