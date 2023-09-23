from flask import Blueprint, render_template, session, jsonify, request, make_response

import heapq

parkinglot = Blueprint("parkinglot", __name__)


def parsing(stro):
    print(stro, "HELP")
    a, b, c = stro.split(",")

    return (a == "B", int(b), int(c))


def calcParking(bS, cS, charges, bus, car, bike):
    if bS == 0 and cS == 0:
        return {
            "Profit": 0,
            "BusRejections": bus,
            "CarRejections": car,
            "BikeRejections": bike,
        }
    res = {}
    profit = 0
    # Check Car slots first -> bus
    cP, biP, buP = charges["Car"], charges["Bike"], charges["Bus"]
    slots = [
        (-1 * cP, "C"),
        (-1 * 5 * biP, "5B"),
        (-1 * buP, "B"),
        (-1 * (cP * 2 + biP * 2), "2C2B"),
        (-1 * cP * 2, "2C"),
        (-1 * (cP + biP * 7), "1C7B"),
        (-1 * biP * 12, "12B"),
    ]

    # allSlots = {
    #     "C": cP,
    #     "5B": 5 * biP,
    #     "B": buP,
    #     "2C2B": cP * 2 + biP * 2,
    #     "2C": cP * 2,
    #     "1C7B": cP + biP * 7,
    #     "12B": biP * 12,
    # }
    heapq.heapify(slots)
    # most to least valuable
    # sortedCSV = {k: v for k, v in sorted(allSlots.items(), key=lambda item: -item[1])}

    # Check optimal slot
    while len(slots) > 0:
        v, s = heapq.heappop(slots)
        if s == "B":
            if bS > 0 and bus > 0:
                bUsed = min(bS, bus)
                profit += bUsed * v
                bS -= bUsed
                bus -= bUsed
        if s == "C":
            if cS > 0 and car > 0:
                cUsed = min(cS, car)
                profit += cUsed * v
                cS -= cUsed
                car -= cUsed
        elif s == "5B":
            if bike > 0 and cS > 0:
                maxU = cS // 5
                bUsed = min(maxU * 5, bike // 5 * 5)
                profit += bUsed // 5 * v
                cS -= bUsed // 5
                bike -= bUsed
                # remainder
                if bike < 5 and bike > 0 and cS > 0:
                    heapq.heappush(slots, (-1 * bike * biP, "C,0,{}".format(bike)))
        elif s == "2C2B":
            if bike > 0 and bS > 0 and car > 0:
                maxU = bS // 2
                bUsed = min(maxU * 2, bike // 2 * 2, car // 2 * 2)
                profit += bUsed // 2 * v
                bS -= bUsed // 2
                bike -= bUsed
                car -= bUsed
                if bike <= 2 and bike >= 0 and bS > 0 and car <= 2 and car >= 0:
                    heapq.heappush(
                        slots,
                        (-1 * (bike * biP + car * cP), "B,{},{}".format(car, bike)),
                    )
        elif s == "2C":
            if bS > 0 and car > 0:
                maxU = bS // 2
                bUsed = min(maxU * 2, car // 2 * 2)
                profit += bUsed // 2 * v
                bS -= bUsed // 2
                car -= bUsed
                if bS > 0 and car <= 2 and car >= 0:
                    heapq.heappush(
                        slots, (-1 * (bike * biP + car * cP), "B,{},0".format(car))
                    )
        elif s == "12B":
            if bike > 0 and bS > 0:
                maxU = bS // 12
                bUsed = min(maxU * 12, bike // 12 * 12)
                profit += bUsed // 12 * v
                bS -= bUsed // 12
                bike -= bUsed
                # remainder
                if bike < 12 and bike > 0 and bS > 0:
                    heapq.heappush(slots, (-1 * bike * biP, "B,0,{}".format(bike)))
        elif s == "1C7B":
            if bike > 0 and bS > 0 and car > 0:
                maxU = bS
                bUsed = min(maxU, bike // 7 * 7, car)
                profit += bUsed * v
                bS -= bUsed
                bike -= bUsed * 7
                car -= bUsed
                if bike <= 7 and bike >= 0 and bS > 0 and car <= 2 and car >= 0:
                    heapq.heappush(
                        slots,
                        (-1 * (bike * biP + car * cP), "B,{},{}".format(car, bike)),
                    )
        else:
            # "These are remainder"
            isBus, c, b = parsing(s)
            if isBus:
                if (bike > 0 or car > 0) and bS > 0:
                    if bike > b and car > c:
                        bike -= b
                        car -= c
                        profit += v
                        bS -= 1
                    else:
                        minB = min(car, c)
                        minC = min(bike, b)
                        if bS > 0:
                            heapq.heappush(
                                slots,
                                (
                                    -1 * (minB * biP + minC * cP),
                                    "B,{},{}".format(minC, minB),
                                ),
                            )
            else:
                if (bike > 0 or car > 0) and cS > 0:
                    if bike > b and car > c:
                        bike -= b
                        car -= c
                        profit += v
                        cS -= 1
                    else:
                        minB = min(car, c)
                        minC = min(bike, b)
                        if cS > 0:
                            heapq.heappush(
                                slots,
                                (
                                    -1 * (minB * biP + minC * cP),
                                    "B,{},{}".format(minC, minB),
                                ),
                            )

    res["Profit"] = profit * -1
    res["BusRejections"] = bus
    res["CarRejections"] = car
    res["BikeRejections"] = bike

    return res


@parkinglot.route("/parking-lot", methods=["POST"])
def getCommon():
    print(request.json)
    busS = request.json["BusParkingSlots"]
    carS = request.json["CarParkingSlots"]
    charge = request.json["ParkingCharges"]
    bus = request.json["Buses"]
    car = request.json["Cars"]
    bike = request.json["Bikes"]

    return jsonify(
        {
            "Answer": calcParking(
                busS, carS, charge, max(bus, 0), max(car, 0), max(bike, 0)
            )
        }
    )
