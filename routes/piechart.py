from flask import Blueprint, render_template, session, jsonify, request, make_response
from math import pi

piechart = Blueprint("piechart", __name__)


def calculateRadians(total, qtys, maxRadians):
    qtys.sort(reverse=True)
    res = [0.0]
    for qty in qtys:
        res.append((qty / total) * maxRadians)
    return {"intruments": qty}


def calcSplitChort():
    pass


@piechart.route("/piechart", methods=["GET"])
def getCommon():
    items = request.json["data"]
    isFirst = request.json["part"] == "FIRST"
    itemMap = {}
    total = 0
    counts = []
    currency = {}
    assetClass = {}
    region = {}
    sector = {}

    for i in items:
        c, a, r, s = i["currency"], i["assectClass"], i["region"], i["sector"]
        val = i["quantity"] * i["price"]
        counts.append(val)
        total += val
        if c in currency:
            currency[c] += val
        else:
            currency[c] = val

        if a in assetClass:
            assetClass[a] += val
        else:
            assetClass[a] = val

        if r in region:
            region[r] += val
        else:
            region[r] = val

        if s in sector:
            sector[c] += val
        else:
            sector[c] = val

    if isFirst:
        return jsonify(calculateRadians(total, counts, 2 * pi))
    else:
        return jsonify(calcSplitChort())
