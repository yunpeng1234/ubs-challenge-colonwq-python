from flask import Blueprint, render_template, session, jsonify, request, make_response
from math import pi

piechart = Blueprint("piechart", __name__)

MIN_CHORD = 0.00314159


def counting(res):
    prev = res[0]
    for i in range(1, len(res)):
        temp = prev
        res[i] += temp
        prev = res[i]
    return res


def calculateRadiansSmallArc(total, qtys, maxRadians, starting):
    qtys.sort()
    res = [starting]
    for qty in qtys:
        if qty / total * maxRadians < MIN_CHORD:
            res.append(res[-1] - MIN_CHORD)
            maxRadians -= MIN_CHORD
            total -= qty
        else:
            res.append(res[-1] - ((qty / total) * maxRadians))

    newR = list(map(lambda x: round(x, 8), res))
    return newR


def calculateRadians(total, qtys, maxRadians):
    qtys.sort()
    res = [7 / 6 * pi]
    for qty in qtys:
        if qty / total < 0.0005:
            res.append(res[-1] + MIN_CHORD)
            maxRadians -= MIN_CHORD
            total -= qty
        else:
            res.append(res[-1] + ((qty / total) * maxRadians))

    newR = list(map(lambda x: round(x, 8), res))
    return {"instruments": newR}


# Write from the back smallest to largest
def calculateRadians2(total, qtys, maxRadians):
    qtys.sort()
    res = [2 * pi]
    counter = 0
    for qty in qtys:
        if qty / total < 0.0005:
            counter += 1
            res.append(res[-1] - MIN_CHORD)
            maxRadians -= MIN_CHORD
            total -= qty
        else:
            res.append(res[-1] - ((qty / total) * maxRadians))
    print(counter, len(qtys))
    newR = list(map(lambda x: round(x, 8), res))
    newR[-1] = 0.0
    return {"instruments": newR[::-1]}


# def checkMinimum(total, min, checkAgainst):
#     if (min / total) <= 1 / 1000:
#         newArcSize = (1 / 1000 * pi) / min * total
#         return (False, newArcSize)
#     return (True, 0)


def calcSplitChord(total, qty, cm, am, rm, sm):
    # Calc instruments

    res = calculateRadians(total, qty, maxRadians=pi * 2 / 3)
    print(res)
    # Get the smallest for each given arc
    cMin = min(cm.values())
    aMin = min(cm.values())
    rMin = min(rm.values())
    sMin = min(sm.values())

    # tempH = {}
    # tempH["c"] = cMin
    # tempH["a"] = aMin
    # tempH["r"] = rMin
    # tempH["s"] = sMin
    # totalArcSize = (2 / 3 - 3 / 1000) * pi
    # count = 4
    # arcSize = {}
    # for k, v in sorted(tempH.items(), key=lambda item: item[1]):
    #     ok, newArc = checkMinimum(total, v, totalArcSize / count)
    #     print(newArc)
    #     if not ok:
    #         totalArcSize -= newArc
    #         arcSize[k] = newArc
    #         count -= 1
    #     else:
    #         arcSize[k] = totalArcSize / count
    rhsArcSize = (2 / 3 - 3 / 1000) * pi / 4
    print(rhsArcSize)
    starts = [(1 / 6) * pi + rhsArcSize]
    for i in range(3):
        starts.append(starts[-1] + rhsArcSize + MIN_CHORD)
    print(starts)
    order = ["c", "s", "a", "r"]
    tag = ["currency", "sector", "assetClass", "region"]
    va = [cm, sm, am, rm]
    currHeader = 1 / 6 * pi
    for i in range(4):
        nums = list(va[i].values())
        temp = calculateRadiansSmallArc(total, nums, rhsArcSize, starts[i])
        res[tag[i]] = temp[::-1]
    return res


@piechart.route("/pie-chart", methods=["POST"])
def getCommon():
    items = request.json["data"]
    isFirst = request.json["part"] == "FIRST"
    total = 0
    counts = []

    currency = {}
    assetClass = {}
    region = {}
    sector = {}

    for i in items:
        c, a, r, s = i["currency"], i["assetClass"], i["region"], i["sector"]
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
            sector[s] += val
        else:
            sector[s] = val

    if isFirst:
        return jsonify(calculateRadians2(total, counts, 2 * pi))
    else:
        return jsonify(
            calcSplitChord(total, counts, currency, assetClass, region, sector)
        )
        #
