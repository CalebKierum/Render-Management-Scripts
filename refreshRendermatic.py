import sys
import os
import pickle
import difflib
import glob
import cv2
import numpy as np
from shutil import copyfile
import caffeine
import shutil
### Stuff for repeating args

reportArgs = ""
argIndex = 1

def __getNextArgOrAsk(message):
    global argIndex
    if (argIndex < len(sys.argv)):
        value = sys.argv[argIndex]
        argIndex += 1
        if ("X" is not value):
            print(message + value)
            return value

    return input(message)


def getNextArgOrAsk(message):
    global reportArgs
    res = __getNextArgOrAsk(message)
    if (res != "X"):
        reportArgs += res + " "
    return res

dockedFolder = getNextArgOrAsk("What is the folder you have mounted capstone4 to? ")
dockedFolder = dockedFolder.replace("~", "/Users/ckierum")
pathAddition = "/production/assets/group_2/shot/"

directory = dockedFolder + pathAddition


# Generally get sub folder list
def getSubFolderList(atPath):
    build = []
    for o in os.listdir(atPath):
        if os.path.isdir(os.path.join(atPath, o)):
            build.append(o)
    return build

# Dig from a specific render to a deeper render folder
def demandGoingFurther(atPath, firstTime):
    atPath += "/"
    subFolders = getSubFolderList(atPath)
    priorities = ["masterLayer", "images"]
    for priority in priorities:
        if priority in subFolders:
            return demandGoingFurther(atPath + priority, False)
    if (firstTime):
        return None
    else:
        return atPath

import frameSequenceTools

def findValidRenderPath(shotFolder):
    rendersFolder = shotFolder + "/renders"
    canidates = []
    if os.path.exists(rendersFolder):
        for o in os.listdir(rendersFolder):
            if os.path.isdir(os.path.join(rendersFolder, o)):
                goFurtherPath = demandGoingFurther(os.path.join(rendersFolder, o), True)
                if (goFurtherPath != None):
                    folderTimestamp = os.path.getmtime(goFurtherPath)
                    fileList = glob.glob(goFurtherPath + "/" + "*.tif")
                    if (len(fileList) == 0):
                        continue
                    shotTimestamp = os.path.getmtime(fileList[0])

                    timestamp = max(folderTimestamp, shotTimestamp)
                    validity = frameSequenceTools.orderedFrames(fileList, "")
                    canidates.append({"SUS":validity["Suspicion"], "TS":timestamp, "PATH":goFurtherPath, "LIST":validity["Frames"], "renderFolder":o})

    bestOne = None
    # Latest valid
    for can in canidates:
        if (can["SUS"] == False and (bestOne is None or bestOne["TS"] < can["TS"])):
            bestOne = can

    # Latest invalid
    if (bestOne == None):
        for can in canidates:
            if (bestOne is None or bestOne["TS"] < can["TS"]):
                bestOne = can

    return bestOne

import safety

shotCount = 0
noRenderCount = 0
corruptedRenderCount = 0

def save_obj(obj, name ):
    with open(name, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name, 'rb') as f:
        return pickle.load(f)

def read_or_new_pickle(path, default):
    if os.path.isfile(path):
        with open(path, "rb") as f:
            try:
                return pickle.load(f)
            except Exception: # so many things could go wrong, can't be more specific.
                pass
    with open(path, "wb") as f:
        pickle.dump(default, f)
    return default

for o in sorted(os.listdir(directory)):
    if os.path.isdir(os.path.join(directory, o)):
        shotCount += 1
        fullPath_ext = directory + o
        renderPath = findValidRenderPath(fullPath_ext)
        if (renderPath == None):
            noRenderCount += 1
            print(o + " has no render found")
        else:
            validity = renderPath["SUS"]
            fileList = renderPath["LIST"]
            firstimg = cv2.imread(fileList[0])
            size = (firstimg.shape[1], firstimg.shape[0])
            renderFolderName = renderPath["renderFolder"]

            metatdataFile = fullPath_ext + "/renderMeta.pkl"
            metadata = read_or_new_pickle(metatdataFile, {})

            refreshMetadata = ""
            if (metadata == renderPath):
                refreshMetadata = " Already Rendered! (Skipped)"

            corruptedStr = ""
            if (validity):
                corruptedRenderCount += 1
                corruptedStr += " CORRUPTED!!! "
            print(o + " has render " + renderFolderName + corruptedStr + " " + str(size[0]) + "x" + str(size[1]) + " " + str(len(fileList)) + " frames " + refreshMetadata)
            if (refreshMetadata != ""):
                continue

            outputToFolder = fullPath_ext + "/" + o + "_ren.avi"
            localTemp = "/Users/ckierum/Assets/Renders/" + o + "_temp.avi"
            safety.safetyAsserts(outputToFolder)


            fourcc = cv2.VideoWriter_fourcc('h','2','6','4')
            out = cv2.VideoWriter(localTemp, fourcc, 24.0, size, True)
            assert(out != None)
            for filename in fileList:
                img = cv2.imread(filename)
                out.write(img)

            out.release()
            out = None
            shutil.move(localTemp, outputToFolder)

            save_obj(renderPath, metatdataFile)




print("======== SUMMARY ========")
renderPerc = (float)(shotCount - noRenderCount) / (float)(shotCount)
print("Rendered Shots: " + str(round(renderPerc * 100)) + " %")

corruptedPerc = (float)(corruptedRenderCount) / (float)(shotCount - noRenderCount)
print("Of those: " + str(round(corruptedPerc * 100))+ "% of them are corrupted")