from flask import Blueprint, render_template, session, jsonify, request, make_response

teleport = Blueprint("teleport", __name__)

import math
import heapq


def distance(o, n):
    ox, oy = o
    nx, ny = n
    return abs(ox - nx) ** 2 + abs(oy - ny) ** 2


def minimum_distance_teleportation(k, p, q):
    # Sort teleportation hubs by their Euclidean distance from the starting point
    # Pair storing hub, location (1 pair only)
    locationClosest = {}
    for hub in p:
        hx, hy = hub
        for location in q:
            ox, oy = location
            if (ox, oy) in locationClosest:
                oldDistance = distance(location, locationClosest[(ox, oy)])
                newDistance = distance(hub, location)
                if newDistance < oldDistance:
                    locationClosest[(ox, oy)] = (hx, hy)
            else:
                locationClosest[(ox, oy)] = (hx, hy)

    distanceSaved = []
    res = 0
    prev = (0, 0)
    for t in q:
        ox, oy = t
        possibleSaved = locationClosest[(ox, oy)]
        noTeleDistance = math.sqrt(distance(prev, t))
        teleDistance = math.sqrt(distance(possibleSaved, t))
        heapq.heappush(distanceSaved, max(noTeleDistance - teleDistance, 0))
        res += noTeleDistance
        prev = t
    k = min(k, len(q))

    possibleSaved = sum(heapq.nlargest(k, distanceSaved))

    return res - possibleSaved


@teleport.route("/teleportation", methods=["POST"])
def getCommon():
    k = request.json["k"]
    p = request.json["p"]
    q = request.json["q"]
    print(k, p, q)
    return jsonify(minimum_distance_teleportation(k, p, q))
