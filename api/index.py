from io import BytesIO

import requests
from flask import Flask, render_template, send_file
from PIL import Image, ImageDraw

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/favicon.ico")
def favicon():
    image_url = "https://avatars.githubusercontent.com/u/122824602?v=4"

    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content)).convert("RGBA")

    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, image.size[0], image.size[1]), fill=255)

    rounded_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
    rounded_image.paste(image, (0, 0), mask=mask)

    icon_io = BytesIO()
    rounded_image = rounded_image.convert("RGBA")
    rounded_image.save(icon_io, format="ICO")
    icon_io.seek(0)

    return send_file(icon_io, mimetype="image/x-icon")
