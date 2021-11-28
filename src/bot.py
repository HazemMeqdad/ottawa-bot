import os
from flask import Blueprint, jsonify, request
from discord_interactions import InteractionResponseFlags, InteractionResponseType, verify_key_decorator, InteractionType
import requests
from . import rest
from .enums import ComponentTypes, ButtonStyles
from .database import Users
import time
from requests import get


interaction = Blueprint("interaction", "bot")

CLIENT_PUBLIC_KEY = os.environ["CLIENT_PUBLIC_KEY"]
CLIENT_ID = os.environ["CLIENT_ID"]

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
                            "type": ComponentTypes.ACTION_ROW,
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
                    ]
                }
            })
        
        elif data["name"] == "title":
            new_title = None
            if data["options"]:
                new_title = data["options"][0]["value"]
            if new_title != None and len(new_title) > 100:
                return jsonify({
                    "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                    "data": {
                        "content": "The number of characters is more than a 100."
                    }
                })
            user = request.json["member"]
            x = Users(user["user"]["id"])
            x.update_where("description", new_title)
            if not new_title:
                return jsonify({
                    "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                    "data": {
                        "content": f"Done reset your bio to `Nothing`"
                    }
                })
            return jsonify({
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {
                    "content": f"Done update your bio to: `{new_title}`"
                }
            })

        elif data["name"] == "profile":
            user_id = list(data["resolved"]["users"].keys())[0]
            user = data["resolved"]["users"][user_id]
            x = Users(int(user_id))
            if not x.info:
                x.insert(user["username"])
            x = x.info
            user_avatar = "https://discord.com/assets/6f26ddd1bf59740c536d2274bb834a05.png"
            if user.get("avatar"):
                user_avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.gif" \
                                if user['avatar'].startswith("a_") \
                                else f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.png"
            return jsonify({
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {
                "embeds": [
                    {
                        "fields": [
                            {
                                "name": "User ID",
                                "value": user_id,
                                "inline": True
                            },
                            {
                                "name": "User Name",
                                "value": user["username"]+user["discriminator"],
                                "inline": True
                            }, {
                                "name": "Thanks Count",
                                "value": f"`{x.get('thanks')}` ✨" if x else "Nothing",
                                "inline": True
                            }, {
                                "name": "Bio",
                                "value": x.get("description") if x.get("description") else "Nothing",
                                "inline": True
                            },
                        ],
                        "thumbnail": {
                            "url": user_avatar
                        },
                        "footer": {
                            "text": user["username"]+user["discriminator"],
                            "icon_url": user_avatar
                        }
                    }
                ]
            }
            })

        elif data["name"] == "info":
            return jsonify({
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {
                    "embeds": [
                        {
                            "description":  "Ottawa bot can help with some programming order like search in npmjs.com & pypi.org and more in future." 
                                            "\nOpen source: https://github.com/HazemMeqdad/ottawa-bot" 
                                            "\nSupport server: https://discord.gg/VcWRRphVQB" 
                                            "\nCreatore by: ottawa team & HAZEM"
                            
                        }
                    ]
                }
            })

        elif data["name"] == "server":
            return jsonify({
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {
                    "content": "Soon",
                    "flags": InteractionResponseFlags.EPHEMERAL
                }
            })

        elif data["name"] == "source":
            return jsonify({
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {
                    "content": "https://github.com/HazemMeqdad/ottawa-bot",
                }
            })

        elif data["name"] == "invite":
            return jsonify({
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {
                    "content": f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&permissions=0&scope=bot%20applications.commands",
                    "flags": InteractionResponseFlags.EPHEMERAL
                }
            })

        elif data["name"] == "help":
            return jsonify({
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {
                    "content": "Just type slash(`/`) and choice OT BOT to show all commands"
                }
            })
        
        elif data["name"] == "acceptcode":
            return jsonify({
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {
                    "content": "soon",
                    "flags": InteractionResponseFlags.EPHEMERAL
                }
            })

        elif data["name"] == "post":
            return jsonify({
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {
                    "content": "soon",
                    "flags": InteractionResponseFlags.EPHEMERAL
                }
            })

        elif data["name"] == "pypi":
            project_name = data["options"][0]["value"]
            re = get(
                f"https://pypi.org/pypi/{project_name}/json",
            )
            if re.status_code == 404:
                return jsonify({
                    "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                    "data": {
                        "content": f"i can't find `{project_name}`",
                        "flags": InteractionResponseFlags.EPHEMERAL
                    }
                })
            res = re.json()
            package: dict = res["info"]
            description = package["description"].replace("```", "") if len(
                package["description"]) >= 500 else package["description"][:500]+"...".replace("```", "")
            return jsonify({
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {
                    "embeds": [
                        {
                            "title": package.get("name")+f"`({package.get('version')})`",
                            "url": package.get("package_url"),
                            "description": f"```md\n{description}\n```",
                            "fields": [
                                {
                                    "name": "Author",
                                    "value": package.get("author") or "Nothing"
                                },
                                {
                                    "name": "Documentation",
                                    "value": package.get("project_urls").get("Documentation") or "Nothing"
                                },
                                {
                                    "name": "Home page",
                                    "value": package.get("project_urls").get("Homepage") or "Nothing"
                                },
                                {
                                    "name": "Releases length",
                                    "value": str(len(res.get("releases"))) or "Nothing"
                                }
                            ]
                        }
                    ]
                }
            })

        elif data["name"] == "npm":
            package_name = data["options"][0]["value"]
            res = requests.get(f"https://api.npms.io/v2/package/{package_name}").json()
            if res.get("code") == "NOT_FOUND":
                return jsonify({
                    "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                    "data": {
                        "content": f"i can't find `{package_name}`",
                        "flags": InteractionResponseFlags.EPHEMERAL
                    }
                })
            npm = res["collected"]["metadata"]
            return jsonify({
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {
                    "embeds": [
                        {
                            "title": npm["name"]+f"`({npm['version']})`",
                            "url": npm["links"]["npm"],
                            "description": npm["description"],
                            "fields": [
                                {
                                    "name": "Author",
                                    "value": npm.get("publisher").get("username") or "Nothing"
                                },
                                {
                                    "name": "Home page",
                                    "value": npm.get("links").get("homepage") or "Nothing"
                                },
                                {
                                    "name": "repository",
                                    "value": npm.get("links").get("repository") or "Nothing"
                                },
                                {
                                    "name": "Releases length",
                                    "value": str(len(npm["releases"]))
                                }
                            ]
                        }
                    ]
                }
            })

        elif data["name"] == "thanks":
            return jsonify({
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {
                    "content": "soon"
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
