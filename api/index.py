from io import BytesIO

import requests
from flask import Flask, render_template, send_file
from PIL import Image, ImageDraw

app = Flask(__name__)


# error handlers
@app.errorhandler(404)
def page_not_found(_):
    return (
        render_template(
            "error.html",
            error_code=404,
            error_msg="Oops! The page you're looking for doesn't exist.",
            title="Page Not Found!",
        ),
        404,
    )


@app.errorhandler(400)
def bad_request(_):
    return (
        render_template(
            "error.html",
            error_code=400,
            error_msg="The server could not understand the request due to invalid syntax.",
            title="Bad Request!",
        ),
        400,
    )


@app.errorhandler(403)
def forbidden(_):
    return (
        render_template(
            "error.html",
            error_code=403,
            error_msg="You don't have permission to access this resource.",
            title="Forbidden!",
        ),
        403,
    )


@app.errorhandler(405)
def method_not_allowed(_):
    return (
        render_template(
            "error.html",
            error_code=405,
            error_msg="The request method is not allowed for the requested URL.",
            title="Method Not Allowed!",
        ),
        405,
    )


@app.errorhandler(408)
def request_timeout(_):
    return (
        render_template(
            "error.html",
            error_code=408,
            error_msg="The server timed out waiting for the request.",
            title="Request Timeout!",
        ),
        408,
    )


@app.errorhandler(500)
def internal_server_error(_):
    return (
        render_template(
            "error.html",
            error_code=500,
            error_msg="The server encountered an internal error and was unable to complete your request.",
            title="Internal Server Error!",
        ),
        500,
    )


@app.errorhandler(502)
def bad_gateway(_):
    return (
        render_template(
            "error.html",
            error_code=502,
            error_msg="The server received an invalid response from the upstream server.",
            title="Bad Gateway!",
        ),
        502,
    )


@app.errorhandler(503)
def service_unavailable(_):
    return (
        render_template(
            "error.html",
            error_code=503,
            error_msg="The server is currently unavailable. Please try again later.",
            title="Service Unavailable!",
        ),
        503,
    )


@app.errorhandler(504)
def gateway_timeout(_):
    return (
        render_template(
            "error.html",
            error_code=504,
            error_msg="The server did not receive a timely response from the upstream server.",
            title="Gateway Timeout!",
        ),
        504,
    )


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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
