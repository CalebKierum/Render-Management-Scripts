import os


def orderedFrames(frames, printNM):

    temp = []
    suspiciouslySmall = []
    suspiciouslyFewFrames = False
    for frame in frames:
        relevantName = frame.split("/")[-1].split(".")[0]
        lastNumber = relevantName.split("_")[-1]
        numString = lastNumber.lstrip("0")

        theInt = 0
        if (numString == ""):
            theInt = 0
        else:
            theInt = int(numString)

        size = os.path.getsize(frame)
        if (size < 200000):
            suspiciouslySmall.append(theInt)

        temp.append({"path": frame, "int": theInt})


    sort = sorted(temp, key=lambda k: k['int'])
    minimum = sort[0]["int"]
    maximum = sort[-1]["int"]
    if (maximum - minimum < 20):
        suspiciouslyFewFrames = True

    suspiciouslyMissing = []
    for i in range(minimum, maximum + 1):
        found = False
        for el in temp:
            if (el["int"] == i):
                found = True
                break
        if not found:
            suspiciouslyMissing.append(i)

    build = []
    for shot in sort:
        build.append(shot["path"])

    if (suspiciouslyFewFrames):
        print(printNM + " had suspiciously few frames " + str(minimum) + "-" + str(maximum))

    if (len(suspiciouslyMissing) != 0):
        print(printNM + " suspiciously missing frames: " + str(suspiciouslyMissing))

    if (len(suspiciouslySmall) != 0):
        print(printNM + " has some frames with suspiciously small sizes may be corrupted " + str(sorted(suspiciouslySmall)))

    return build

