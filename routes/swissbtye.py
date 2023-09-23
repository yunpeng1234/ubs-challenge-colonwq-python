from flask import Blueprint, jsonify, request

swissbyte = Blueprint("swissbyte", __name__)


# return line,failed?, env
def traverseNested(code, line, env):
    while line < len(code):
        codeLine = code[line]
        if codeLine.startswith("if "):
            # find the next line
            condtoeval = " ".join(codeLine.split(" ")[1:])
            if not eval(condtoeval, {}, env):
                while code[line] != "endif":
                    line += 1
            newLine, isFailed, newEnv = traverseNested(code, line + 1, env)
            if not isFailed:
                line = newLine
                env = newEnv
            else:
                return (line + 1, True, newEnv)
            continue
        if codeLine == "endif":
            return (line + 1, False, env)
        if codeLine == "fail":
            return (line + 1, True, env)
        else:
            exec(codeLine, {}, env)
            line += 1
    return (line + 1, False, env)


# code = ["a = a + 4", "b = b - 4", "if a == 4", "fail", "endif", "c = 7"]
# o = {"a": 0, "b": 2, "c": 3}
# global_env = {}
# for x, y in o.items():
#     global_env[x] = y
# print(traverseNested(code, 0, global_env))


@swissbyte.route("/swissbyte", methods=["POST"])
def getCommon():
    code = request.json["code"]
    cases = request.json["cases"]
    res = []
    print(code)
    for o in cases:
        print(o)
        global_env = {}
        for x, y in o.items():
            global_env[x] = y
        _, isFailed, env = traverseNested(code, 0, global_env)

        res.append({"is_solvable": not isFailed, "variables": env})

    return jsonify({"outcomes": res})
