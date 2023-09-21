from flask import Blueprint, render_template, session, abort, request, jsonify
from typing import Dict, List


def getNextProbableWords(
    classes: List[Dict], statements: List[str]
) -> Dict[str, List[str]]:
    # Fill in your solution here and return the correct output based on the given input
    classList = set(map(lambda x: list(x.keys())[0], classes))
    ## Also can be polymorphic since it is the same
    emptyClass = set()
    combined = {}

    # Get all the empty classes/ Polymorphic Type
    for c in classes:
        className = list(c.keys())[0]
        value = c[className]
        combined[className] = value
        if isinstance(value, list):
            ## Check all the values in the class list, if so it is poly morphic
            isPoly = True
            for toCheck in value:
                if toCheck not in classList:
                    isPoly = False
            if isPoly:
                emptyClass.add(className)
        elif isinstance(value, Dict):
            continue
        ## empty string
        else:
            emptyClass.add(list(c.keys())[0])

    res = {}
    for statement in statements:
        if statement == "":
            res[statement] = [""]
            continue

        endsWithStop = statement[-1] == "."
        params = statement.split(".")
        filt = ""
        if not endsWithStop:
            filt = params[-1]
        params = params[:-1]
        temp = combined

        # Navigate into params
        for param in params:
            if param in emptyClass:
                res[statement] = [""]
                break
            if param in temp:
                temp = temp[param]
            else:
                ## cannot be found
                res[statement] = [""]
                break

        if statement in res:
            continue

        def isStringAClass(string):
            for c in classList:
                if c in string:
                    return c
            return ""

        def finalise(tocheck, filter):
            if isinstance(temp, list):
                filteredArray = filter(lambda x: x.startswith(filt), temp)
                res[statement] = (
                    sorted(filteredArray)[:5]
                    if len(temp) >= 5
                    else sorted(filteredArray)
                )
            elif isinstance(temp, Dict):
                filteredArray = filter(lambda x: x.startswith(filt), temp.keys())
                res[statement] = (
                    sorted(filteredArray)[:5]
                    if len(temp) >= 5
                    else sorted(filteredArray)
                )
            else:
                res[statement] = [""]

        if isinstance(temp, str) and isStringAClass(temp) != "":
            c = isStringAClass(temp)
            if c in emptyClass:
                res[statement] = [""]
                continue
            temp = combined[c]

        finalise(temp, filter)
    print(res)
    return res


lazydev = Blueprint("lazydev", __name__)


@lazydev.route("/lazy-developer", methods=["POST"])
def getCommon():
    classes = request.json["classes"]
    query = request.json["statements"]
    return jsonify(getNextProbableWords(classes=classes, statements=query))
