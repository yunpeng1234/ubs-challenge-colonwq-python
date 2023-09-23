from flask import Blueprint, render_template, session, jsonify, request, make_response

import heapq

parkinglot = Blueprint("parkinglot", __name__)


def parsing(stro):
    a, b, c = stro.split(",")

    return (a == "B", int(b), int(c))


def pushOptimal(car, bike, cc, bc):
    # try 2, 2
    a, b = min(car, 2), min(bike, 2)
    vA = a * cc + b * bc
    # try 1, 7
    c, d = min(car, 1), min(bike, 7)
    vB = c * cc + d * bc
    if vA >= vB:
        return (-1 * vA, "B,{},{}".format(min(car, 1), min(bike, 7)))
    return (-1 * vB, "B,{},{}".format(min(car, 2), min(bike, 2)))


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
        print(s)
        if s == "B":
            if bS > 0 and bus > 0:
                bUsed = min(bS, bus)
                profit += bUsed * v
                bS -= bUsed
                bus -= bUsed
            continue
        if s == "C":
            if cS > 0 and car > 0:
                cUsed = min(cS, car)
                profit += cUsed * v
                cS -= cUsed
                car -= cUsed
            continue
        elif s == "5B":
            if bike > 0 and cS > 0:
                maxU = bike // 5
                bUsed = min(maxU, cS)
                profit += bUsed * v
                cS -= bUsed
                bike -= bUsed * 5
                # remainder
                if bike < 5 and bike > 0 and cS > 0:
                    heapq.heappush(slots, (-1 * bike * biP, "C,0,{}".format(bike)))
            continue
        elif s == "2C2B":
            if bike > 0 and bS > 0 and car > 0:
                bUsed = min(bS, bike // 2, car // 2)
                profit += bUsed * v
                bS -= bUsed
                bike -= bUsed * 2
                car -= bUsed * 2
                if bike == 0 and car == 0:
                    continue
                if bike >= 0 and bS > 0 and car >= 0:
                    heapq.heappush(
                        slots,
                        pushOptimal(car, bike, cP, biP),
                    )

            continue
        elif s == "2C":
            if bS > 0 and car > 0:
                bUsed = min(bS, car // 2)
                profit += bUsed * v
                bS -= bUsed
                car -= bUsed * 2
                if bS > 0 and car < 2 and car > 0:
                    heapq.heappush(
                        slots, (-1 * (bike * biP + car * cP), "B,{},0".format(car))
                    )
            continue
        elif s == "12B":
            if bike > 0 and bS > 0:
                bUsed = min(bS, bike // 12)
                profit += bUsed * v
                bS -= bUsed
                bike -= bUsed * 12
                # remainder

                if bike < 12 and bike > 0 and bS > 0:
                    heapq.heappush(slots, (-1 * bike * biP, "B,0,{}".format(bike)))

            continue
        elif s == "1C7B":
            if bike > 0 and bS > 0 and car > 0:
                maxU = bS
                bUsed = min(maxU, bike // 7, car)
                profit += bUsed * v
                bS -= bUsed
                bike -= bUsed * 7
                car -= bUsed
                if bike == 0 and car == 0:
                    continue
                if bike >= 0 and bS > 0 and car >= 0:
                    heapq.heappush(
                        slots,
                        pushOptimal(car, bike, cP, biP),
                    )
            continue
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
                            print("B,{},{}".format(minC, minB), s)
                continue
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
                            print("B,{},{}".format(minC, minB), s)

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
                max(busS, 0),
                max(carS, 0),
                charge,
                max(bus, 0),
                max(car, 0),
                max(bike, 0),
            )
        }
    )
