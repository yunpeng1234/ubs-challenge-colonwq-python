from flask import Blueprint, render_template, session, jsonify, request, make_response

chinesewall = Blueprint("chinesewall", __name__)


@chinesewall.route("/chinese-wall", methods=["GET"])
def getCommon():
    return jsonify(
        {
            "1": "Fluffy",
            "2": "Galactic",
            "3": "Mangoes",
            "4": "Subatomic",
            "5": "Jellyfish",
        }
    )
