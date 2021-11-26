from flask import Flask
from src.bot import interaction
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.register_blueprint(interaction)

if __name__ == "__main__":
    app.run("0.0.0.0")
