import logging
from controllers.Credential import Credential
from flask import Blueprint, request, jsonify

credential = Blueprint("credential", __name__)
credential_controller = Credential()

@credential.route("/", methods=["GET"])
def get_all_credentials():
    try:
        creds = credential_controller.get_all_credentials()
        return jsonify(creds), 200
    except Exception as err:
        logging.exception("not able to get all credentials with err : {}".format(err.__str__()))
        return jsonify({"error": err.__str__()}), 500


@credential.route("/", methods=["POST"])
def create_credential():
    if not request.is_json:
        return jsonify({"error": "only json request is accepted"}), 400

    try:
        cred = request.get_json()
        credential_controller.create_credential(cred)
        return jsonify({}), 201
    except ValueError as err:
        logging.exception("failed to create new credential with : {}".format(err.__str__()))
        return jsonify({"error": err.__str__()}), 400
    except Exception as err:
        logging.exception("not able to create new credentials with err : {}".format(err.__str__()))
        return jsonify({"error": err.__str__()}), 500
