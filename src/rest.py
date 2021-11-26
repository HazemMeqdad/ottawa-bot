from __future__ import annotations
import os
from typing import Any
import requests
from .enums import ApplicationCommandTypes


TOKEN = os.environ.get("TOKEN")
BASE = "https://discord.com/api/v9"

application_id = os.environ.get("CLIENT_ID")
guild_id = os.environ.get("GUILD_ID")


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


def create_command(
    name: str,
    description: str,
    options: list[dict] = [],
    type: ApplicationCommandTypes | int = 1
):
    return request(
        "POST",
        f"/applications/{application_id}/guilds/{guild_id}/commands",
        json={
            "name": name,
            "description": description,
            "options": options,
            "type": type
        }
    )


def delete_command(command_id, /):
    request(
        "DELETE",
        f"/applications/{application_id}/guilds/{guild_id}/commands/{command_id}"
    )


def edit_command(command_id, **kwargs: Any):
    data = {item: value for item, value in kwargs if item in [
        "name", "description", "options"]}
    return request(
        "PATCH",
        f"/applications/{application_id}/guilds/{guild_id}/commands/{command_id}",
        json=data
    )

def create_invite(channel_id: int, target_application_id: int):
    return request("POST", f"/channels/{channel_id}/invites", json={"max_age": 0, "target_type": 2, "target_application_id": target_application_id})


