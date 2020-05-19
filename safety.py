import os
def safetyAsserts(pathToWriteTo):
    lastBit = pathToWriteTo.split("/")[-1]
    directory = "/".join(pathToWriteTo.split("/")[:-1])

    # Directory exists
    assert(os.path.exists(directory))

    # Directory is long
    assert(len(directory) > 10)

    # Name is long
    assert(len(lastBit) > 4)

    # Last bit does not start in dot
    assert(lastBit[0] != ".")

    # last bit ends in mp4 or avi
    assert(lastBit.endswith("mp4") or lastBit.endswith("avi"))

    # No double dots in it
    assert(pathToWriteTo.find("..") == -1)

    assert(pathToWriteTo[-1] != "/")
    assert(pathToWriteTo[-1] != ".")