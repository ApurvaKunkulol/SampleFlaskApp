from flask import Flask, url_for, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def index():
    paragraph = """
                    But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was 
                    born and I will give you a complete account of the system, and expound the actual teachings of the 
                    great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or 
                    avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue 
                    pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone 
                    who loves or pursues or desires to obtain pain of itself, because it is pain, but because 
                    occasionally circumstances occur in which toil and pain can procure him some great pleasure. 
                    To take a trivial example, which of us ever undertakes laborious physical exercise, except to 
                    obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy 
                    a pleasure that has no annoying consequences, or one who avoids a pain that produces no 
                    resultant pleasure?
    """
    message = ""
    template_variables = {"message": message, "paragraph": paragraph}
    return render_template("hello.html", **template_variables)


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
