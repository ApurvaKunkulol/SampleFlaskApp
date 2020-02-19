from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from markupsafe import escape
from .constants import local_connection_string


app = Flask(__name__)
app.config["MONGO_URI"] = local_connection_string
mongo = PyMongo(app)


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
    message = "This is a place holder for the title message."
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


@app.route("/showdb")
def show_db():
    return "The name of the current database is <strong>{}</strong>".format(str(mongo.db.name))


@app.route("/insert", methods=["GET", "POST"])
def insert_rec():
    if request.method == "POST":
        status = mongo.db.user.insert(request.json)
        if status is not None:
            return "Record inserted successfully.<br/>ID of the inserted record: <strong>{}</strong>".format(status)
        else:
            return "Error while inserting record."


@app.route("/edit", methods=["POST", "PUT"])
def update_rec():
    if request.method == "PUT":
        search_param = request.json.get("email")
        if search_param is None or "":
            return "No search term found.<br><br>Please provide one in the request body."
        existing_record = mongo.db.user.find({"email": search_param})[0]
        updated_info = request.json.get("updated_info")
        for key, value in updated_info.items():
            if key in existing_record:
                existing_record[key] = value
        status = mongo.db.user.update({"_id": existing_record.get("_id")}, existing_record)

        if status is not None:
            return "Record updated successfully."
        else:
            return "Error while updating record."


@app.route("/delete", methods=["DELETE"])
def delete_rec():
    if request.method == "DELETE":
        search_param = request.json.get("email")
        if search_param is None or "":
            return "No search term found.<br><br>Please provide one in the request body."
        deletion_status = mongo.db.user.delete_one({"email": search_param})

        if deletion_status is not None:
            return "Record deleted successfully."
        else:
            return "Error while deleting record."
