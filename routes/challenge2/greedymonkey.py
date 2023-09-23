from flask import Blueprint, render_template, session, jsonify, request, make_response
import time


greedymonkey = Blueprint("greedymonkey", __name__)


def getFruit(max_weight, max_volume, fruit):
    n = len(fruit)
    dp = [[[0] * (max_volume + 1) for _ in range(max_weight + 1)] for _ in range(n + 1)]

    for i in range(n + 1):
        for w in range(max_weight + 1):
            for v in range(max_volume + 1):
                weight, volume, value = fruit[i - 1]
                if i == 0 or w == 0 or v == 0:
                    dp[i][w][v] = 0
                elif weight <= w and volume <= v:
                    dp[i][w][v] = max(
                        dp[i - 1][w][v],
                        dp[i - 1][w - weight][v - volume] + value,
                    )
                else:
                    dp[i][w][v] = dp[i - 1][w][v]
    return dp[-1][-1][-1]


# f = [[110, 80, 60], [80, 155, 90]]
# print(getFruit(100, 150, f))


@greedymonkey.route("/greedymonkey", methods=["POST"])
def getCommon():
    w = request.json["w"]
    v = request.json["v"]
    f = request.json["f"]
    print(w, v, f)
    ans = getFruit(w, v, f)
    return jsonify(ans)
