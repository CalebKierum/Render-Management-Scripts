import sys
import os
import pickle
import difflib
import glob
import cv2
import numpy as np
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
        print("This folder " + fullPath + " we expected to have frames... but did not")
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


def findLatestRenderFolders(shotFolder, oldTS):
    rendersFolder = shotFolder + "/renders"
    if os.path.exists(rendersFolder):
        timestamps = getFolderToTimestampDictionaryGoingFurther(rendersFolder + "/")
        if (len(timestamps) == 0):
            return None

        #latest = max(timestamps, key=timestamps.get)
        build = []
        for folder in timestamps:
            if (timestamps[folder] > oldTS):
                build.append({"Folder": folder, "Path": demandGoingFurther(rendersFolder + "/" + folder, True), "timestamp":timestamps[folder]})

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
            renderPaths = findLatestRenderFolders(fullPath_ext, oldTS)
            if renderPaths is not None:
                #renderAge = os.path.getmtime(renderPath)
                #build[o] = {"renderFolder": renderPath, "age":renderAge}
                build[o] = renderPaths
            else:
                build[o] = {"NONE":"NONE"}

    return build



#print(getLastestRenderFolderDictionary(directory))
#oldTS = load_obj( "tListDict3")
oldTS = 0
newDict = getLastestRenderFolderDictionary(directory, oldTS)
print(newDict)
newList = []
for key in newDict:
    if not "NONE" in newDict[key]:
        if not key in oldDict:
            newList.append(key)
        elif "NONE" in oldDict[key]:
            newList.append(key)
        elif oldDict[key]["age"] < newDict[key]["age"]:
            newList.append(key)

print()
print("New renders appear to be: " + str(newList))
print()
if (len(newList) == 0):
    print("There appear to be no shots and we dont support all yet so.....")
    sys.exit(1)

request = getNextArgOrAsk("List shots from above you want to render OR allnew OR all: ")
renderList = []
if request.lower() == "all":
    print("NOT SUPPORTED")
elif request.lower() == "allnew":
    renderList = newList
else:
    # PARSE the listp
    parts = request.lower().split(",")
    for part in parts:
        renderList.append(difflib.get_close_matches(part, newList, n=1)[0])


print()
print("Will render: " + str(renderList))
print()

outputFolder = getNextArgOrAsk("What should the output folder be (or press enter for script default): ")
if ("" == outputFolder or "def" == outputFolder):
    outputFolder = "/Users/ckierum/Assets/Renders/"



def compositeFramesInFolder(pathWithShots, outputToFolder):

    print("Writing images in " + pathWithShots + " to " + outputToFolder)
    if not pathWithShots.endswith('/'):
        pathWithShots += "/"

    fileList = sorted(glob.glob(pathWithShots + "*.tif"))

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


for render in renderList:
    compositeFramesInFolder(newDict[render]["renderFolder"], outputFolder+render+".mp4")


saveAsk = getNextArgOrAsk("Do you want to save that you did this render? {y/n}")
if (saveAsk == "y"):
    print("Saving!!!")
    save_obj(newDict, "tListDict2")

print("Ok we are done.")