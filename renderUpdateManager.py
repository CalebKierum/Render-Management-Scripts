import sys
import os
import pickle
import difflib
import glob
import cv2
import numpy as np
from shutil import copyfile
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
print("Reading all the shot folders (this may take awhile)")
dockedFolder = dockedFolder.replace("~", "/Users/ckierum")
pathAddition = "/production/assets/group_2/shot/"

directory = dockedFolder + pathAddition

# Generally get the timestamp to folder names at path
def getFolderToTimestampDictionary(atPath):
    dictionary = {}
    for o in os.listdir(atPath):
        if os.path.isdir(os.path.join(atPath, o)):
            fullPath = atPath + o
            dictionary[o] = os.path.getmtime(fullPath)
    return dictionary

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

def timestampOfFolderORFileInFolder(fullPath):
    fileList = glob.glob(fullPath + "/" + "*.tif")
    if (len(fileList) == 0):
        #print("This folder " + fullPath + " we expected to have frames... but did not")
        return None
    else:
        return os.path.getmtime(fileList[0])
    return os.path.getmtime(fullPath)

# Going furhter
def getFolderToTimestampDictionaryGoingFurther(atPath):
    dictionary = {}
    for o in os.listdir(atPath):
        if os.path.isdir(os.path.join(atPath, o)):
            goFurther = demandGoingFurther(atPath + o, True)
            if goFurther is None:
                continue
            fullPath = goFurther

            timestamp = timestampOfFolderORFileInFolder(fullPath)
            if (timestamp is None):
                continue

            dictionary[o] = timestamp
    return dictionary

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def findLatestRenderFolders(shotFolder, oldTS, shotName):
    rendersFolder = shotFolder + "/renders"
    if os.path.exists(rendersFolder):
        timestamps = getFolderToTimestampDictionaryGoingFurther(rendersFolder + "/")
        if (len(timestamps) == 0):
            return None

        #latest = max(timestamps, key=timestamps.get)
        build = []
        for folder in timestamps:
            if (timestamps[folder] > oldTS):
                build.append({"Folder": folder, "Path": demandGoingFurther(rendersFolder + "/" + folder, True), "timestamp":timestamps[folder], "shot": shotName})

        if (len(build) == 0):
            return None

        return build

    else:
        return None

def getLastestRenderFolderDictionary(fullPath, oldTS):
    build = {}
    for o in sorted(os.listdir(fullPath)):
        if os.path.isdir(os.path.join(fullPath, o)):
            fullPath_ext = fullPath + o
            renderPaths = findLatestRenderFolders(fullPath_ext, oldTS, o)
            if renderPaths is not None and len(renderPaths) != 0:
                #renderAge = os.path.getmtime(renderPath)
                #build[o] = {"renderFolder": renderPath, "age":renderAge}
                build[o] = renderPaths

    return build



#print(getLastestRenderFolderDictionary(directory))
#oldTS = load_obj( "timeStamp")
oldTS = load_obj( "timeStamp")
newDict = getLastestRenderFolderDictionary(directory, oldTS)
print("Found: " + str(newDict))
potentialRenderString = ""

print()
print("New renders appear to be:")
for key in newDict:
    for el in newDict[key]:
        print("\t" + key + "/" + el["Folder"])


print()

request = getNextArgOrAsk("List shots from above you want to render, allnew, and/or all: ")
renderList = []

for request in request.split(","):
    if (request.lower() == "all"):
        print("Preparing this may take some time.....")
        considerationDict = getLastestRenderFolderDictionary(directory, 0)
        for key in considerationDict:
            for el in considerationDict[key]:
                renderList.append(el)
    elif request.lower() == "allnew":
        for key in newDict:
            for el in newDict[key]:
                renderList.append(el)
    else:
        reqParts = request.split("/")
        if (len(reqParts) > 2):
            print("Cant handle " + request)
        elif (len(reqParts) == 2):
            # there is a subpath
            fullPath_ext = directory + reqParts[0] + "/renders/" + reqParts[1]
            print("Fullpath ext " + fullPath_ext)
            found = {"Folder": reqParts[1], "Path": demandGoingFurther(fullPath_ext, True), "timestamp":timestampOfFolderORFileInFolder(demandGoingFurther(fullPath_ext, True)), "shot":reqParts[0]}
            renderList.append(found)
        else:
            # this better be a shots folder
            if (request in newDict):
                for el in newDict[request]:
                    renderList.append(el)
            else:
                # Fuzzy search keys
                fuzzed = False
                for key in newDict:
                    if request in key:
                        for el in newDict[key]:
                            fuzzed = True
                            renderList.append(el)

                if (fuzzed):
                    continue

                # This is an old shots folder
                fullPath_ext = directory + request
                renderPaths = findLatestRenderFolders(fullPath_ext, 0, request)
                if (renderPaths is None or len(renderPaths) == 0):
                    print("Cant handle " + request + " no render folders found her?")
                for path in renderPaths:
                    renderList.append(path)



print()
print("Will render: " + str(renderList))
print()

outputFolder = getNextArgOrAsk("What should the output folder be (or press enter for script default): ")
if ("" == outputFolder or "def" == outputFolder):
    outputFolder = "/Users/ckierum/Assets/Renders/"



import frameSequenceTools
def compositeFramesInFolder(pathWithShots, outputToFolder, shortName):

    print("Writing images in " + pathWithShots + " to " + outputToFolder)
    if not pathWithShots.endswith('/'):
        pathWithShots += "/"

    fileList = frameSequenceTools.orderedFrames(glob.glob(pathWithShots + "*.tif"), shortName)

    if (len(fileList) == 0):
        print("FOR SOME REASON FOUND 0 images at " + pathWithShots)
        print("We will therefore skip this")
        return

    firstimg = cv2.imread(fileList[0])
    size = (firstimg.shape[1], firstimg.shape[0])


    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter(outputToFolder, fourcc, 24.0, size, True)
    assert(out != None)
    for filename in fileList:


        img = cv2.imread(filename)
        out.write(img)

    out.release()
    out = None
    return ""

import safetyAsserts

maxDict = {}
for render in renderList:
    folder = render["Folder"]
    path = render["Path"]
    timestamp = render["timestamp"]
    shot = render["shot"]
    outputPath = outputFolder+shot+"_" +folder + ".mp4"

    safetyAsserts.safetyAsserts(outputPath)

    compositeFramesInFolder(path, outputPath, shot + "/" + folder)
    if (not shot in maxDict):
        maxDict[shot] = {"ts":timestamp, "path":outputPath}
    else:
        prev = maxDict[shot]["ts"]
        if (timestamp > prev):
            maxDict[shot] = {"ts":timestamp, "path":outputPath}




putShotsInCapstoneFolder = getNextArgOrAsk("Put these renders in the capstone folder? {y/n}")
if (putShotsInCapstoneFolder == "y"):
    for shot in maxDict:
        pathToPutIn = directory + shot + "/" + shot + "_ren.mp4"
        pathItIsAt = maxDict[shot]["path"]

        # SAFETY ASSERTS
        safetyAsserts.safetyAsserts(pathToPutIn)

        copyfile(pathItIsAt, pathToPutIn)


saveAsk = getNextArgOrAsk("Do you want to save that you did this render? {y/n}")
if (saveAsk == "y"):
    print("Saving!!!")
    maxTS = 0
    for key in maxDict:
        ts = maxDict[key]["ts"]
        if (ts > maxTS):
            maxTS = ts
    save_obj(maxTS, "timeStamp")

print("Ok we are done.")