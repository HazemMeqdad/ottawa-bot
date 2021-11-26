from __future__ import annotations
from typing import Any
from .rest import request
import os
import requests
from enum import Enum


application_id = os.environ.get("CLIENT_ID")
guild_id = os.environ.get("GUILD_ID")


class ApplicationCommandTypes(Enum):
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3

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


def check_commands():
    json_commands = requests.get(
        "https://gist.githubusercontent.com/HazemMeqdad/3e4171446c48f801e83f3241b7876c2e/raw/b3a337702c6ca26b8df3266bb3a0ab4e5d05d025/commands.json").json()

    commands = request(
        "GET",
        f"/applications/{application_id}/guilds/{guild_id}/commands"
    )
    print(commands)
    for command in json_commands:
        if command["name"] not in [i["name"] for i in commands]:
            print(command["name"])
            x = create_command(**command)
            print(x)

    for command in commands:
        if command["name"] not in [i["name"] for i in json_commands]:
            delete_command(command["id"])

	# for command in json_commands:
	# 	data = [i for i in commands if i["name"] == command["name"]]
	# 	if command["name"] != data["name"] or command["description"] != data["description"] or command["options"] != data["options"]:
	# 		edit_command(command["id"], **data)


# check_commands()
x = create_command("ping", "Ping pong !!")
print(x)
