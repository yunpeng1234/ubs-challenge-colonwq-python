from flask import Blueprint, render_template, session, jsonify, request, make_response
from math import pi

piechart = Blueprint("piechart", __name__)


def counting(res):
    prev = res[0]
    for i in range(1, len(res)):
        temp = prev
        res[i] += temp
        prev = res[i]
    return res


def calculateRadians(total, qtys, maxRadians):
    qtys.sort(reverse=True)
    res = [0.0]
    for qty in qtys:
        print(qty / total)
        print(maxRadians * qty / total)

        res.append((qty / total) * maxRadians)
    counting(res)
    print(res)
    newR = list(map(lambda x: round(x, 8), res))
    return {"instruments": newR}


# Write from the back smallest to largest
def calculateRadians2(total, qtys, maxRadians):
    qtys.sort()
    res = [2 * pi]
    for qty in qtys:
        if qty / total < 0.0005:
            res.append(res[-1] - 0.00314159)
            maxRadians -= 0.00314159
            total -= qty
        else:
            res.append(res[-1] - ((qty / total) * maxRadians))
    newR = list(map(lambda x: round(x, 8), res))
    return {"instruments": newR[::-1]}


def checkMinimum(total, min, checkAgainst):
    if (min / total) <= 1 / 1000:
        newArcSize = (1 / 1000 * pi) / min * total
        return (False, newArcSize)
    return (True, 0)


def calcSplitChort(total, qty, cm, am, rm, sm):
    res = {}
    # Calc instruments
    rhsArcSize = (2 / 3 - 3 / 1000) * pi / 4

    tempR = calculateRadians(total, qty, maxRadians=pi * 2 / 3)["instruments"][::-1]
    qty = list(map(lambda x: x + (pi * (7 / 6)), tempR))
    res["instruments"] = qty

    # Get the smallest for each given arc
    cMin = min(cm.values())
    aMin = min(cm.values())
    rMin = min(rm.values())
    sMin = min(sm.values())

    tempH = {}
    tempH["c"] = cMin
    tempH["a"] = aMin
    tempH["r"] = rMin
    tempH["s"] = sMin
    totalArcSize = (2 / 3 - 3 / 1000) * pi
    count = 4
    arcSize = {}
    for k, v in sorted(tempH.items(), key=lambda item: item[1]):
        ok, newArc = checkMinimum(total, v, totalArcSize / count)
        print(newArc)
        if not ok:
            totalArcSize -= newArc
            arcSize[k] = newArc
            count -= 1
        else:
            arcSize[k] = totalArcSize / count
    order = ["c", "s", "a", "r"]
    tag = ["currency", "sector", "assetClass", "region"]
    va = [cm, sm, am, rm]
    currHeader = 1 / 6 * pi
    for i in range(4):
        arcS = arcSize[order[i]]
        nums = list(va[i].values())
        temp = calculateRadians(total, nums, arcS)["instruments"]
        tmp = list(
            map(
                lambda x: round(x, 8),
                map(
                    lambda x: x + currHeader,
                    temp,
                ),
            )
        )
        res[tag[i]] = tmp
        currHeader += arcS + (1 / 1000 * pi)
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
            sector[c] += val
        else:
            sector[c] = val

    if isFirst:
        print(sorted(counts), total)
        return jsonify(calculateRadians2(total, counts, 2 * pi))
    else:
        return jsonify({})
        # calcSplitChort(total, counts, currency, assetClass, region, sector)
