from flask import Blueprint, render_template, session, jsonify, request, make_response

maze = Blueprint("maze", __name__)

oldMaze = ""
endX = None
endY = None
trace = []
saved = {}
deads = {}
currX = 0
currY = 0

# {
#   "mazeId": "3f184088-31fd-4231-a404-f76e257b8d0e",
#   "nearby": [
#     [0, 0, 0],
#     [0, 3, 1],
#     [0, 0, 1]
#   ],
#   "mazeWidth": 4,
#   "step": 0,
#   "isPreviousMovementValid": false,
#   "message": ""
# }

moves = ["up", "down", "left", "right"]
offset = {"up": [1, 0], "down": [-1, 0], "left": [0, -1], "right": [0, 1]}

# 0 	wall cell 	x
# 1 	empty cell 	v
# 2 	spawn cell 	v
# 3 	end cell 	v


def solve(mazeId, nearby, mazeWidth, step, isPreviousMovementValid, message):
    global oldMaze
    global endX
    global endY
    global trace
    global saved
    global deads
    global currX
    global currY

    if mazeId != oldMaze:
        trace = []
        oldMaze = mazeId
        endX = None
        endY = None
        saved = {}
        deads = {}
        currX = 0
        currY = 0

    isDead = True
    oldMove = "respawn"
    newX = 1
    newY = 0
    move = "down"

    # prepare to backtrack
    if len(trace) > 0:
        oldMove = trace[-1]
        newX = currX
        newY = currY
        move = "respawn"
        if oldMove == "up":
            move = "down"
            newY -= 1
        elif oldMove == "down":
            move = "up"
            newY += 1
        elif oldMove == "left":
            move = "right"
            newX += 1
        elif oldMove == "right":
            move = "left"
            newX -= 1

    currG = 0
    if (currX, currY) in saved:
        currG = saved[(currX, currY)] + 1

    for i in moves:
        offsetX = offset[i][0]
        offsetY = offset[i][1]
        x = currX + offsetX
        y = currY + offsetY

        # square is a dead end
        if (x, y) in deads:
            continue
        # square is a wall
        if nearby[offsetX + 1][offsetY + 1] == 0:
            continue

        # end cell
        if nearby[offsetX + 1][offsetY + 1] == 3:
            endX = x
            endY = y
            newX = x
            newY = y
            move = i
            isDead = False
            return move  # TODO: terminate later

        # shorter path, or not visited
        #  or saved[(x,y)] > currG ignore shorter for now
        if nearby[offsetX + 1][offsetY + 1] == 1 and (x, y) not in saved:
            isDead = False
            saved[(x, y)] = currG
            newX = x
            newY = y
            move = i
            break

    # pop trace!!!!
    if isDead:
        deads[(currX, currY)] = True
        trace.pop()

    currX = newX
    currY = newY
    return {"playerAction": move}


# print(solve("A", [
#     [0, 0, 0],
#     [0, 3, 1],
#     [0, 0, 0]
#   ], None, None, None, None))
# print(solve("A", [
#     [0, 0, 0],
#     [3, 1, 0],
#     [0, 0, 0]
#   ], None, None, None, None))


@maze.route("/maze", methods=["POST"])
def getCommon():
    mazeId = request.json["mazeId"]
    nearby = request.json["nearby"]
    mazeWidth = request.json["mazeWidth"]
    step = request.json["step"]
    isPreviousMovementValid = request.json["isPreviousMovementValid"]
    message = request.json["message"]
    return jsonify(
        solve(mazeId, nearby, mazeWidth, step, isPreviousMovementValid, message)
    )
