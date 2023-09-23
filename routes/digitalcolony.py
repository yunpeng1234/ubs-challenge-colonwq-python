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
    # Will be a key of (x,y) : count
    currGen = {}
    for i in range(len(currentGeneration) - 1):
        x = currentGeneration[i]
        y = currentGeneration[i + 1]
        if (x, y) in currGen:
            currGen[(x, y)] += 1
        else:
            currGen[(x, y)] = 1
    for i in range(generation):
        tempGeneration = {}
        newWeight = ans
        for x, y in currGen.keys():
            counter = currGen[(x, y)]
            new = (ans % 10 + sig[x][y]) % 10

            if (x, new) in tempGeneration:
                tempGeneration[(x, new)] += counter
            else:
                tempGeneration[(x, new)] = counter

            if (new, y) in tempGeneration:
                tempGeneration[(new, y)] += counter
            else:
                tempGeneration[(new, y)] = counter
            # tempGeneration.append(new)

            newWeight += new * counter
        currGen = tempGeneration
        ans = newWeight
    return str(ans)


@digitalcolony.route("/digital-colony", methods=["POST"])
def getCommon():
    w = request.json
    arrayReq = []
    for o in w:
        arrayReq.append(getGeneration(int(o["generations"]), o["colony"]))
    return jsonify(arrayReq)
