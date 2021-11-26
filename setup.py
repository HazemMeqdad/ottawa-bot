import os
import requests
import time
from dotenv import load_dotenv
load_dotenv()
from src import rest


commands = requests.get(
    "https://gist.githubusercontent.com/HazemMeqdad/432d6712e19e3007756e94130eb46891/raw/38aa8e76030b782957e72aedf1f022ce295603d9/commands.json").json()
application_id = os.environ.get("CLIENT_ID")

globles_command = ["ping", "source", "invite", "pypi", "npm", "help"]


for command in commands:
    if command["name"] in globles_command:
        rest.request(
            "POST",
            f"/applications/{application_id}/commands",
            json=command
        )
        time.sleep(3)
        continue
    x = rest.create_command(**command)
    print(x)
    time.sleep(3)
    
print("done processing commands")
