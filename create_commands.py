from __future__ import annotations
from src.discord import request
from src.enums import ApplicationCommandTypes
import config


application_id = config.CLIENT_ID
guild_id = config.GUILD_ID

commands = request(
    "GET", 
    f"/applications/{application_id}/guilds/{guild_id}/commands"
)

for command in commands:
    request(
        "DELETE", f"/applications/{application_id}/guilds/{guild_id}/commands/{command.get('id')}")

def create_command(
    name: str, 
    description: str, 
    options: list[dict] = [], 
    type: ApplicationCommandTypes = 1
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





