from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

if __name__ == '__main__':
    app.run(debug=True)
