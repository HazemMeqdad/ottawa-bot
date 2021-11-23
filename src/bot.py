import os
from flask import Blueprint, jsonify, request
from .verify import verify_key_decorator
from .enums import InteractionType, InteractionResponseType, InteractionResponseFlags
from .discord import create_invite 
import config


interaction = Blueprint("interactions", "bot")


CLIENT_PUBLIC_KEY = config.CLIENT_PUBLIC_KEY


@interaction.route('/interactions', methods=['POST'])
@verify_key_decorator(CLIENT_PUBLIC_KEY)
def interactions():
    data = request.json.get("data")
    if request.json['type'] == InteractionType.APPLICATION_COMMAND:
        if data["name"] == "youtube":
            invite = create_invite()
            return jsonify({
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {
                    "content": "Hello world"
                }
            })
    elif request.json['type'] == InteractionType.MESSAGE_COMPONENT:
        return jsonify({
            'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            'data': {
                'content': 'Hello, you interacted with a component.',
                'flags': InteractionResponseFlags.EPHEMERAL
            }
        })
