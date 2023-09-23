from flask import Blueprint, jsonify, request
from collections import deque


digitalcolony = Blueprint("digitalcolony", __name__)


def getGeneration(generation, colony):
    currentGeneration = [int(digit) for digit in colony]
    ans = sum(currentGeneration)
    sig = [
        [0, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        [1, 0, 9, 8, 7, 6, 5, 4, 3, 2],
        [2, 1, 0, 9, 8, 7, 6, 5, 4, 3],
        [3, 2, 1, 0, 9, 8, 7, 6, 5, 4],
        [4, 3, 2, 1, 0, 9, 8, 7, 6, 5],
        [5, 4, 3, 2, 1, 0, 9, 8, 7, 6],
        [6, 5, 4, 3, 2, 1, 0, 9, 8, 7],
        [7, 6, 5, 4, 3, 2, 1, 0, 9, 8],
        [8, 7, 6, 5, 4, 3, 2, 1, 0, 9],
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
    ]
    for i in range(generation):
        tempGeneration = []
        newWeight = ans
        for j in range(len(currentGeneration) - 1):
            curr = currentGeneration[j]
            nxt = currentGeneration[j + 1]
            tempGeneration.append(currentGeneration[j])

            new = (ans % 10 + sig[curr][nxt]) % 10

            tempGeneration.append(new)

            newWeight += new

        tempGeneration.append(currentGeneration[-1])
        currentGeneration = tempGeneration
        ans = newWeight
        print(i)
    return ans


print(getGeneration(50, "1000"))


@digitalcolony.route("/digital-colony", methods=["POST"])
def getCommon():
    w = request.json
    arrayReq = []
    for o in w:
        arrayReq.append(getGeneration(int(o["generations"]), o["colony"]))
    # r = make_response(getFruit(w, v, f), 200)
    # r.mimetype = "text/plain"
    return jsonify(arrayReq)
