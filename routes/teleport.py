from flask import Blueprint, render_template, session, jsonify, request, make_response

teleport = Blueprint("teleport", __name__)

import math


def minimum_distance_teleportation(k, p, q):
    # Sort teleportation hubs by their Euclidean distance from the starting point
    p.sort(key=lambda hub: math.sqrt(hub[0] ** 2 + hub[1] ** 2))

    total_distance = 0.0
    remaining_items = q.copy()

    while remaining_items:
        if k > 0:
            # Use a teleportation orb if available
            closest_hub = p.pop(0)
            k -= 1
        else:
            # Walk to the nearest teleportation hub
            closest_hub = min(
                p,
                key=lambda hub: math.sqrt(
                    (hub[0] - remaining_items[0][0]) ** 2
                    + (hub[1] - remaining_items[0][1]) ** 2
                ),
            )

        # Calculate the Euclidean distance from the current location to the next item's location
        distance = math.sqrt(
            (closest_hub[0] - remaining_items[0][0]) ** 2
            + (closest_hub[1] - remaining_items[0][1]) ** 2
        )

        # Update total distance and remove the delivered item from the list
        total_distance += distance
        remaining_items.pop(0)

    return round(total_distance, 2)


@teleport.route("/teleportation", methods=["POST"])
def getCommon():
    k = request.json["k"]
    p = request.json["p"]
    q = request.json["q"]

    return jsonify(minimum_distance_teleportation(k, p, q))
