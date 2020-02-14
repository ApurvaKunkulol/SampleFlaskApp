from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def index():
    return "Hi! I am Flask, a Micro Web framework!!"


@app.route("/hello")
def hello():
    return "This is the Hello World URL."


@app.route("/user/<username>")
def parameterised_view(username):
    return "The entered username is {}".format(escape(username) if username else "Unspecified")


@app.route("/post/<float:post_id>")
def converter_type_view(post_id):
    return "Received post ID: {}".format(post_id if post_id else "N/A - improper type.")


@app.route("/projects/")
def project_page():
    return "The Project Page."


@app.route("/about")
def about_page():
    return "<h2>The About page.</h2>"
