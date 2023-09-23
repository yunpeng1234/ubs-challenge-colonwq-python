from flask import Blueprint, jsonify, request

swissbyte = Blueprint("swissbyte", __name__)


@swissbyte.route("/swissbyte", methods=["POST"])
def getCommon():
    w = request.json["code"]
    variables = request.json
    global_env = {}

    for o in w:
        pass

    return jsonify("arrayReq")
