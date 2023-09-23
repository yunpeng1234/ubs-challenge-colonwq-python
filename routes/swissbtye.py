from flask import Blueprint, jsonify, request

swissbyte = Blueprint("swissbyte", __name__)


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
        vtoCount = set()
        env = {}
        for x, y in o.items():
            env[x] = y
            vtoCount.add(x)

        # return line,failed?, env
        def traverseNested(code, line):
            while line < len(code):
                codeLine = code[line]
                if codeLine.startswith("if "):
                    # find the next line
                    condtoeval = " ".join(codeLine.split(" ")[1:])
                    line += 1
                    if not eval(condtoeval, env):
                        endifcount = 1
                        while endifcount != 0:
                            if code[line].startswith("if "):
                                endifcount += 1
                            if code[line] == "endif":
                                endifcount -= 1
                            line += 1
                    newLine, isFailed = traverseNested(code, line)
                    if not isFailed:
                        line = newLine
                    else:
                        return (line + 1, True)
                    continue
                if codeLine == "endif":
                    return (line + 1, False)
                if codeLine == "fail":
                    return (line + 1, True)
                else:
                    exec(codeLine, env)
                    line += 1
            return (line + 1, False)

        _, isFailed = traverseNested(code, 0)

        extracted = {}
        for v in vtoCount:
            extracted[v] = env[v]

        res.append({"is_solvable": not isFailed, "variables": extracted})

    return jsonify({"outcomes": res})
