import sys
import os
import glob
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

## The actual script
renderFolder = getNextArgOrAsk("What is the path to the render folder? ")
if (not renderFolder.endswith("/")):
    renderFolder += "/"

## Check for images subolder
imagesFolder = renderFolder + "images/"
if (not os.path.exists(imagesFolder)):
    print("You need to have this subfolder exists " + imagesFolder)
    assert(False)

## Loop through layers
import frameSequenceTools

for o in sorted(os.listdir(imagesFolder)):
    if os.path.isdir(os.path.join(imagesFolder, o)):
        if (o != "tmp"):
            fullPath_ext = imagesFolder + o
            fileList = glob.glob(fullPath_ext + "/" + "*.tif")

            validity = frameSequenceTools.orderedFrames(fileList, fullPath_ext)
            frames = validity["Frames"]

            subFolder = fullPath_ext + "/ordered"
            if (os.path.exists(subFolder)):
                # Clear folder
                os.rmdir(subFolder)

            os.mkdir(subFolder)


            for (idx, frame) in enumerate(frames):
                endName = frame.rsplit('/', 1)[-1]
                copyfile(frame, subFolder + "/" + str(idx) + endName)



