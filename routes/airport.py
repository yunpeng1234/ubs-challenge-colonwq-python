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


# def mergeSort(arr):
#     if len(arr) > 1:
#         # Finding the mid of the array
#         mid = len(arr) // 2
#         # Dividing the array elements
#         L = arr[:mid]

#         # Into 2 halves
#         R = arr[mid:]

#         # Sorting the first half
#         mergeSort(L)

#         # Sorting the second half
#         mergeSort(R)

#         i = j = k = 0

#         while i < len(L) and j < len(R):
#             if L[i].askTimeToDeparture() <= R[j].askTimeToDeparture():
#                 arr[k] = L[i]
#                 i += 1
#             else:
#                 arr[k] = R[j]
#                 j += 1
#             k += 1

#         # Checking if any element was left
#         while i < len(L):
#             arr[k] = L[i]
#             i += 1
#             k += 1

#         while j < len(R):
#             arr[k] = R[j]
#             j += 1
#             k += 1


def merge(arr, start, mid, end):
    start2 = mid + 1

    # If the direct merge is already sorted
    if arr[mid].askTimeToDeparture() <= arr[start2].askTimeToDeparture():
        return

    # Two pointers to maintain start
    # of both arrays to merge
    while start <= mid and start2 <= end:
        # If element 1 is in right place
        if arr[start].askTimeToDeparture() <= arr[start2].askTimeToDeparture():
            start += 1
        else:
            value = arr[start2]
            index = start2

            # Shift all the elements between element 1
            # element 2, right by 1.
            while index != start:
                arr[index] = arr[index - 1]
                index -= 1

            arr[start] = value

            # Update all the pointers
            start += 1
            mid += 1
            start2 += 1


def mergeSort(arr, l, r):
    if l < r:
        # Same as (l + r) / 2, but avoids overflow
        # for large l and r
        m = l + (r - l) // 2

        # Sort first and second halves
        mergeSort(arr, l, m)
        mergeSort(arr, m + 1, r)

        merge(arr, l, m, r)


def prioritisation_function(passengers, cut_off_time):
    okToUse = []
    for p in passengers:
        if p.askTimeToDeparture() >= cut_off_time:
            okToUse.append(p)
    mergeSort(okToUse)
    # your solution here
    # return sorted array of passenger instances
    return okToUse


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
