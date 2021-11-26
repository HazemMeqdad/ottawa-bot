from __future__ import annotations
import os
from typing import Any
import requests


TOKEN = os.environ.get("TOKEN")
BASE = "https://discord.com/api/v9"


def request(method: str, rout: str, *args, **kwargs) -> dict | None | Any:
    re = requests.request(
        method, 
        BASE+rout,
        headers={
            "Authorization": f"Bot {TOKEN}",
            "content-type": "application/json"
        },
        *args, 
        **kwargs
    )
    try:
        return re.json()
    except:
        return None


def create_invite(channel_id: int, target_application_id: int):
    return request("POST", f"/channels/{channel_id}/invites", json={"max_age": 0, "target_type": 2, "target_application_id": target_application_id})
