import os
from flask import Blueprint, jsonify, request
from discord_interactions import InteractionResponseFlags, InteractionResponseType, verify_key_decorator, InteractionType
from . import rest
from .enums import ComponentTypes, ButtonStyles

interaction = Blueprint("interaction", "bot")

CLIENT_PUBLIC_KEY = os.environ["CLIENT_PUBLIC_KEY"]


@interaction.route("/interactions", methods=["POST"])
@verify_key_decorator(CLIENT_PUBLIC_KEY)
def interactions():
    data = request.json.get("data")
    if request.json["type"] == InteractionType.APPLICATION_COMMAND:
        if data["name"] == "ping":
            return jsonify({
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {
                    "content": "pong",
                    "components": [
                        {
                            "type": ComponentTypes.BUTTON,
                            "custom_id": "pong",
                            "style": ButtonStyles.PRIMARY,
                            "emoji": {
                                "id": None, 
                                "name": "🏓"
                            }
                        }
                    ]
                }
            })
    elif request.json["type"] == InteractionType.MESSAGE_COMPONENT:
        return jsonify({
            "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            "data": {
                "content": "Hello, you interacted with a component.",
                "flags": InteractionResponseFlags.EPHEMERAL
            }
        })
