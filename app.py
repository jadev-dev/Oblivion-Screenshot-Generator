from os import listdir
import random
from flask import Flask
from flask import render_template
from flask import request
from flask import Response
from generator import make_image

APP = Flask(__name__, template_folder="./www")


@APP.route("/", methods=['POST', 'GET'])
def input_page():
    npc_list = [file for file in sorted(listdir("./faces")) if not file[0] == "."]
    if request.method == 'POST':
        user_selections = request.form
        generated_image = make_image(user_selections.get("input_text"), user_selections.get("npc_choice"))
        return render_template("generator.html", encoded_image=generated_image.decode("utf-8"), npc_list=npc_list)
    else:
        return render_template("generator.html", encoded_image=None, npc_list=npc_list)

@APP.route("/style.css", methods=['GET'])
def style_sheet():
    pan_directions = [["left", "right"], ["right", "left"]]
    y_position = random.randint(25, 75)
    pan_position = random.choice(pan_directions)
    return Response(render_template("style.css", pan_position=pan_position, y_position=y_position), mimetype="text/css")
