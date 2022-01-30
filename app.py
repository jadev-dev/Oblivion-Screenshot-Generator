from flask import Flask
from generator import make_image

APP = Flask(__name__)


@APP.route("/<npc_name>/<input_text>")
def index(npc_name=None, input_text=None):
    return f'<h1>success:</h1> <img src="data:image/png;base64, {make_image(input_text, npc_name).decode("utf-8")}">'

