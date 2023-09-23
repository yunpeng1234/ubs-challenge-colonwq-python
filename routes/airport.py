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
def partition(arr, first, last, start, mid):
    pivot = arr[last].askTimeToDeparture()
    end = last

    # Iterate while mid is not greater than end.
    while mid[0] <= end:
        # Inter Change position of element at the starting if it's value is less than pivot.
        if arr[mid[0]].askTimeToDeparture() < pivot:
            arr[mid[0]], arr[start[0]] = arr[start[0]], arr[mid[0]]

            mid[0] = mid[0] + 1
            start[0] = start[0] + 1

        # Inter Change position of element at the end if it's value is greater than pivot.
        elif arr[mid[0]].askTimeToDeparture() > pivot:
            arr[mid[0]], arr[end] = arr[end], arr[mid[0]]

            end = end - 1

        else:
            mid[0] = mid[0] + 1


# Function to sort the array elements in 3 cases
def quicksort(arr, first, last):
    # First case when an array contain only 1 element
    if first >= last:
        return

    # Second case when an array contain only 2 elements
    if last == first + 1:
        if arr[first].askTimeToDeparture() > arr[last].askTimeToDeparture():
            arr[first], arr[last] = arr[last], arr[first]

            return

    # Third case when an array contain more than 2 elements
    start = [first]
    mid = [first]

    # Function to partition the array.
    partition(arr, first, last, start, mid)

    # Recursively sort sublist containing elements that are less than the pivot.
    quicksort(arr, first, start[0] - 1)

    # Recursively sort sublist containing elements that are more than the pivot
    quicksort(arr, mid[0], last)


def prioritisation_function(passengers, cut_off_time):
    okToUse = []
    for p in passengers:
        if p.askTimeToDeparture() >= cut_off_time:
            okToUse.append(p)
    quicksort(okToUse, 0, len(okToUse) - 1)
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
