from flask import Blueprint, jsonify, request

airport = Blueprint("airport", __name__)


# Simple passenger class
class Passenger:
    def __init__(self, departureTime):
        self.departureTime = departureTime
        self.numberOfRequests = 0

    def askTimeToDeparture(self):
        self.numberOfRequests += 1
        return self.departureTime

    def getNumberOfRequests(self):
        return self.numberOfRequests


def execute(prioritisation_function, passenger_data, cut_off_time, test_id):
    totalNumberOfRequests = 0
    passengers = []

    # Initialise list of passenger instances
    for i in range(len(passenger_data)):
        passengers.append(Passenger(passenger_data[i]))

    # Apply solution and re-shuffle with departure cut-off time
    prioritised_and_filtered_passengers = prioritisation_function(
        passengers, cut_off_time
    )

    # Sum totalNumberOfRequests across all passengers
    for i in range(len(passengers)):
        totalNumberOfRequests += passengers[i].getNumberOfRequests()
    print("totalNumberOfRequests: " + str(totalNumberOfRequests))

    # Print sequence of sorted departure times
    print("Sequence of prioritised departure times:")
    prioritised_filtered_list = []
    for i in range(len(prioritised_and_filtered_passengers)):
        print(prioritised_and_filtered_passengers[i].departureTime, end=" ")
        prioritised_filtered_list.append(
            prioritised_and_filtered_passengers[i].departureTime
        )

    print("\n")
    return {
        "id": test_id,
        "numberOfRequests": totalNumberOfRequests,
        "sortedDepartureTimes": prioritised_filtered_list,
    }


def swap(a, i, j):
    temp = a[i]
    a[i] = a[j]
    a[j] = temp


def firstParition(a, low, high, i, j, cutOff):
    # To handle 2 elements
    if high - low <= 1:
        if a[high].askTimeToDeparture() < a[low].askTimeToDeparture():
            swap(a, high, low)
        i = low
        j = high
        return (i, j)

    mid = low
    pivot = cutOff
    while mid <= high:
        toCheck = a[mid].askTimeToDeparture()
        if toCheck < pivot:
            swap(a, low, mid)
            low += 1
            mid += 1
        elif toCheck == pivot:
            mid += 1
        elif toCheck > pivot:
            swap(a, mid, high)
            high -= 1

    # update i and j
    i = low - 1
    j = mid  # or high+1
    return (i, j)


def partition(a, low, high, i, j):
    # To handle 2 elements
    if high - low <= 1:
        if a[high].askTimeToDeparture() < a[low].askTimeToDeparture():
            swap(a, high, low)
        i = low
        j = high
        return (i, j)

    mid = low
    pivot = a[high].askTimeToDeparture()
    while mid <= high:
        toCheck = a[mid].askTimeToDeparture()
        if toCheck < pivot:
            swap(a, low, mid)
            low += 1
            mid += 1
        elif toCheck == pivot:
            mid += 1
        elif toCheck > pivot:
            swap(a, mid, high)
            high -= 1

    # update i and j
    i = low - 1
    j = mid  # or high+1
    return (i, j)


# 3-way partition based quick sort
def quickSort(a, low, high):
    if low >= high:  # 1 or 0 elements
        return

    i = low
    j = high

    # Note that i and j are passed as reference
    i, j = partition(a, low, high, i, j)

    # Recur two halves
    quickSort(a, low, i)
    quickSort(a, j, high)


# 3-way partition based quick sort
def fquickSort(a, low, high, cutOff):
    if low >= high:  # 1 or 0 elements
        return

    i = low
    j = high

    # Note that i and j are passed as reference
    i, j = firstParition(a, low, high, i, j, cutOff)

    quickSort(a, j, high)
    return i


def prioritisation_function(passengers, cut_off_time):
    # okToUse = []
    # for p in passengers:
    #     temp = p.askTimeToDeparture()
    #     if temp >= cut_off_time:
    #         okToUse.append(p)
    i = fquickSort(passengers, 0, len(passengers) - 1, cut_off_time)
    # your solution here
    # return sorted array of passenger instances
    return passengers[i + 1 :]


@airport.route("/airport", methods=["POST"])
def getCommon():
    w = request.json
    print(w)
    arrayReq = []
    for o in w:
        arrayReq.append(
            execute(
                prioritisation_function,
                o["departureTimes"],
                o["cutOffTime"],
                o["id"],
            )
        )
    return jsonify(arrayReq)
