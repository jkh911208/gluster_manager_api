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

    node = request.get_json()
    try:
        resource_controller.discover_new_node(node)
        return jsonify({}), 201
    except paramiko.AuthenticationException as err:
        logging.exception("Authentication to node : {} failed, please check you credential".format(node["address"]))
        return jsonify({"error": err.__str__()}), 401
    except Exception as err:
        logging.exception("Not able to discover new node with error : {}".format(err.__str__()))
        return jsonify({"error": err.__str__()}), 500

@resource.route("/", methods=["GET"])
def get_all_nodes():
    try:
        nodes = resource_controller.get_all_nodes()
        return jsonify(nodes), 200
    except Exception as err:
        logging.exception("not able to get all nodes from data with error : {}".format(err.__str__()))
        return jsonify({"error": err.__str__()}), 500 

@resource.route("/", methods=["DELETE"])
def delete_one_node():
    if not request.is_json:
        return jsonify({"error": "only json request is accepted"}), 400

    node_id = request.get_json()
    try:
        deleted = resource_controller.delete_one_node(node_id)
        return jsonify({"deleted": True}), 200
    except Exception as err:
        logging.exception("not able to get all nodes from data with error : {}".format(err.__str__()))
        return jsonify({"error": err.__str__()}), 500 