import logging

from flask import Flask, request
from flask_restplus import Api, Resource
from .project_start import mongo
from bson import json_util
from email_validator import validate_email, EmailNotValidError, EmailSyntaxError
from werkzeug.exceptions import BadRequest


app = Flask(__name__)
api = Api(app)


@api.route("/hello_api/<string:email>")
class HelloAPI(Resource):
    def get(self, email):
        """
        Description: Will get the user information associated with the passed email.
        Parameters:
            email: The email ID of the user whose information is required.
        Return:
             JSON containing the information of the user.
             e.g:
             {
                "_id" : ObjectId("5e4a81de2c2fc0c10b7d336e"),
                "firstname" : "Akshay",
                "lastname" : "Panini",
                "email" : "panini.akshay@gmail.com",
                "designation" : "student",
                "address" : "Varanasi, India.",
                "website" : "https://someURL.com",
                "qualification" : "M. Phil (History)"
            }

            In case of an error it'll still return a JSON indicating the unsuccessful status of the operation.
            e.g: {"error": "No user found with the given email."}
        """

        try:
            validation_status = validate_email(email)
            email = validation_status.get("email")
        except EmailNotValidError as email_err:
            logging.error("Error while validating given email.", exc_info=True)
            return {"status": "error", "description": "Email is not in proper format."}
        except Exception as ex:
            logging.error("Error in email validation.", exc_info=True)
            return {"status": "error", "description": "Email validation error."}

        tmp = mongo.db.user.find({"email": email})
        try:
            existing_user = tmp[0]
        except IndexError as index_err:
            logging.error("Error while accessing records for existing user.", exc_info=True)
            return {"status": "error", "description": "No user found with the given email."}
        except Exception as ex:
            logging.error("Error while accessing existing records.", exc_info=True)
            return {"status": "error", "description": "Exception while retrieving the user: <br><p>{}</p>".format(str(ex))}
        if existing_user:
            return json_util.dumps({"status": "success", "description": "", "user_info": existing_user})

    def put(self, email):
        """
        Description: A PUT function whose primary objective is to update information of the user with the information
                     received in the request body. However, if there is no existing record of the user, it will insert a
                     new record for the user.
                     An example of the updated info would be:
                        {
                            "updated_info": {
                                "firstname" : "Apurva",
                                "lastname" : "Kunkulol",
                                "email" : "kunkulol.apurva@gmail.com",
                                "designation" : "student",
                                "address" : "Bombay, India.",
                                "website" : "https://someURL.com",
                                "qualification" : "M. Arch (Restoration Architecture)"
                            }

                        }
        Parameter(s):
            email: String containing the email of the user whose information to edit.
        Return:
            JSON containing the status of the operation.
            example: { "status": "Record updated successfully." }
        """
        try:
            if email:
                try:
                    validation_status = validate_email(email)
                    email = validation_status.get("email")
                except EmailNotValidError as email_err:
                    logging.error("Error while validating given email.", exc_info=True)
                    return {"status": "error", "description": "Email is not in proper format."}
                except Exception as ex:
                    logging.error("Error in email validation.", exc_info=True)
                    return {"status": "error", "description": "Email validation error."}

                if email:
                    tmp = mongo.db.user.find({"email": email})
                    try:
                        existing_record = tmp[0]
                        updated_info = request.json.get("updated_info")
                        if updated_info:
                            for key, value in updated_info.items():
                                if key == "email":
                                    continue
                                existing_record[key] = value
                            result = mongo.db.user.update({"email": email}, existing_record)
                            if "ok" in result:
                                return {"status": "success", "description": "Record updated successfully."}
                            else:
                                return {"status": "error", "description": "Could not update record successfully. "
                                                                          "Status description: {}".format(result)}
                        else:
                            return {"status": "error", "description": "Please supply information to update."}
                    except IndexError as idx_err:
                        logging.warning("No previous record exists for {}. Inserting a new one.".format(email))
                        inserted_id = mongo.db.user.insert(request.json.get("updated_info"))
                        return {"status": "error", "description": "Inserted a new record successfully since a previous "
                                                                  "one didn't exist for this email. ID: "
                                                                  "{}".format(inserted_id)}
            else:
                return {"status": "error", "description": "Email address not supplied."}
        except Exception as ex:
            logging.error("Error while updating information about {}".format(email), exc_info=True)
            return {"status": "error", "description": "Error while updating information. "
                                                      "Please contact support for more information."}

    def delete(self, email):
        """
        Description:
            A DELETE function to delete user information associated with the email supplied.
        Parameter(s):
            email: Email address of the user whose record to delete.
        Returns:
            JSON containing the status of the operation.
        """
        if email:
            try:
                validation_status = validate_email(email)
                email = validation_status.get("email")
                if email:
                    result = mongo.db.user.delete_one({"email": email})
                    deleted_count = result.deleted_count
                    if deleted_count == 1:
                        return {"status": "success", "description": "Successfully deleted information for user "
                                                                    "{}.".format(email)}
                    elif deleted_count < 1:
                        return {"status": "error", "description": "User does not exist for email {}.".format(email)}
            except EmailNotValidError as email_err:
                logging.error("Error while validating the email {}".format(email), exc_info=True)
                return {"status": "error", "description": "Validation Error. There was an error validating the email "
                                                          "{}".format(email)}
            except Exception as ex:
                logging.error("Error while deleting info for the email {}".format(email), exc_info=True)
                return {"status": "error", "description": "Error while deleting info for the email {}".format(email)}
        else:
            return {"status": "error", "description": "Please provide the email of the user whose record to delete."}


@api.route("/hello_api/create")
class CreateUser(Resource):
    def post(self):
        """
        Will only create a new record for the user if none exists.
        Make a request from POSTMAN(or any other REST client for that matter.) in the following form:

        URL: 127.0.0.1:5000/hello_api/create (replace the loopback IP with the IP of the server that you're
                                              running from)
        BODY of the request:
            As shown below.
            Please select Body > raw > JSON in the UI of the REST Client.
        Arguments:
            Dictionary/JSON inside the `.json` attribute of the request.
            e.g:
                {
                    "firstname" : "abc",
                    "lastname" : "pqr",
                    "email" : "pqr.abc@gmail.com",
                    "designation" : "student",
                    "address" : "someplace, somecountry.",
                    "website" : "https://someURL.com",
                    "qualification" : "M. Phil (History)"
                }

        Return:
            JSON containing the status of the operation.
        """
        try:
            if request.json:
                try:
                    if "email" in request.json:
                        tmp = mongo.db.user.find({"email": request.json.get("email")})
                        existing_user = None
                        try:
                            existing_user = tmp[0]
                            return {"status": "error", "description": "User with email {} "
                                                                      "already exists.".format(request.json.get("email"))}
                        except IndexError as iderr:
                            inserted_id = mongo.db.user.insert(request.json)
                            return {"status": "success", "description": "Successfully inserted record for user. "
                                                                        "ID: {}".format(inserted_id)}
                        except Exception as ex:
                            logging.error("Error while attempting to retrieve existing record", exc_info=True)
                            return {"status": "error",
                                    "description": "Error while inserting information for the user "
                                                   "{}.".format(request.json.get("email"))}
                    else:
                        return {"status": "error",
                                "description": "Please provide email. It is a mandatory field."}
                except Exception as ex:
                    logging.error("Error while inserting record for email {}.".format(request.json.get("email")),
                                  exc_info=True)
                    return {"status": "error", "description": "Error while inserting record."}
        except BadRequest as bad_req_err:
            logging.error("Input error.", exc_info=True)
            return {"status": "error", "description": "No or bad  input provided."}


if __name__ == "__main__":
    app.run(debug=True)
