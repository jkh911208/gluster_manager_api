from flask import Blueprint, request

credential = Blueprint("credential", __name__)

@credential.route("/")
def hello_world():
    return "hello_world"
