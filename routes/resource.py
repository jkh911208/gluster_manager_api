import logging
from controllers.Resource import Resource
from flask import Blueprint, request, jsonify
import paramiko

resource = Blueprint("resource", __name__)
resource_controller = Resource()

@resource.route("/", methods=["POST"])
def discover_new_node():
    if not request.is_json:
        return jsonify({"error": "only json request is accepted"}), 400

    try:
        node = request.get_json()
        resource_controller.discover_new_node(node)
        return jsonify({}), 201
    except paramiko.AuthenticationException as err:
        logging.exception("Authentication to node : {} failed, please check you credential".format(node["address"]))
        return jsonify({"error": err.__str__()}), 401
    except Exception as err:
        logging.exception("Not able to discover new node with error : {}".format(err.__str__()))
        return jsonify({"error": err.__str__()}), 500
