import cv2
import numpy as np
import glob
import time
import os
from progressbar import ProgressBar
pbar = ProgressBar()
import shutil
import sys

#sshfs -p 22 kieruc@attu.cs.washington.edu:/projects/instr/capstone4 ~/localSync
sshfsFolder = "/Users/ckierum/localSync"
shotsFolder = sshfsFolder+ "/production/lighting/paths/NewTry/images"
examplePath = shotsFolder + "/seq_01_intro_0200/images/"


outputPath = "/Users/ckierum/Assets/"

def extractPotentialShotTitleFromPath(path):
    seqAt = path.rfind("seq_")
    if seqAt is -1:
        return "res99.mp4"
    else:
        slashBefore = seqAt
        slashEnd = path.find("/", seqAt + 1)
        print("IND " + str(slashBefore) + " to " + str(slashEnd))
        return path[slashBefore:slashEnd] + ".mp4"

def getOutputPathOrPath(path):
    if outputPath is None:
        return path
    else:
        return outputPath

def compositeFramesInFolder(path):
    print("Path: " + path)
    if not path.endswith('/'):
        path += "/"


    fileList = sorted(glob.glob(path + "*.tif"))
    print("Path: ", path, "Discovred: ", len(fileList), "files")
    print("Reading: " + fileList[0])
    firstimg = cv2.imread(fileList[0])
    size = (firstimg.shape[1], firstimg.shape[0])
    print("It has size")

    print("Write to: " + path + extractPotentialShotTitleFromPath(path))
    #fourcc = cv2.VideoWriter_fourcc('h','2','6','4') #->AVI
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter(getOutputPathOrPath(path) + extractPotentialShotTitleFromPath(path), fourcc, 24.0, size, True)
    print("WRITING " + getOutputPathOrPath(path) + extractPotentialShotTitleFromPath(path))
    print("Writing!")
    #print(fileList)
    for filename in fileList:
        #print("Read pic: " + filename)
        img = cv2.imread(filename)
        out.write(img)

    out.release()
    out = None

def renderShots(shotsFolder, name, outputfolder=None):
    if shotsFolder.endswith('/'):
        print("Cant render here as path ends with slash!", path)
        return

    folderList = sorted(glob.glob(shotsFolder + "/*"))
    for folder in folderList:
        print()
        shotname = folder[len(shotsFolder)+1:]
        print("Folder/Shotname: ", shotname)

        print(folder + "/" + name)
        if os.path.isdir(folder + "/" + name):
            build = folder + "/" + name
            if os.path.isfile(build + "/res.mp4"):
                print("Already rendered")
            else:
                try:
                    compositeFramesInFolder(build)
                    print("Done Succesfully!")
                    if outputfolder is not None:
                        shutil.copyfile(build + "/res.mp4", outputfolder + "/" + shotname + ".mp4")
                        print("Copied out")
                except:
                    print("Failed")
        else:
            print("Does not have images folder")


first = True
for arg in sys.argv:
    if first:
        first = False
    else:
        print("=====PROCESSING " + str(arg) + " ========")
        compositeFramesInFolder(str(arg))

#print(extractPotentialShotTitleFromPath("/Users/ckierum/localSync/mousetrap/group06/asset/shots/seq_02_cheese_0300/br/images/masterLayer"))


#compositeFramesInFolder(shotsFolder + "/seq_02_cheese_0300/final/images")
#enderShots(shotsFolder, "final/images/", outputfolder=shotsFolder + "/finalRender/")
#compositeFramesInFolder(shotsFolder + "/seq_01_intro_0100/rf/images/BG")
#
#print("REAL")
#/Users/ckierum/localSync/mousetrap/group06/asset/shots/seq_01_intro_0100/final/images/intro_0100_0037.tif
#compositeFramesInFolder(shotsFolder + "/seq_03_sneak_out_0200/final/images")
#compositeFramesInFolder(shotsFolder + "/seq_06_reunited_0400/final/images")
#compositeFramesInFolder(shotsFolder + "/seq_06_reunited_0400/t1/images/masterLayer/render_cam")
#compositeFramesInFolder(shotsFolder + "/seq_07_end_0400/final/images")
#compositeFramesInFolder("/Users/ckierum/localSync3/production/lighting/paths" + "/at5/images/Everything")
#compositeFramesInFolder("/Users/ckierum/localSync3/production/lighting/paths" + "/at6/images/Everything")
#compositeFramesInFolder("/Users/ckierum/localSync3/production/lighting/paths" + "/at7/images/Everything")
#compositeFramesInFolder("/Users/ckierum/localSync3/production/lighting/paths" + "/at8/images/Everything")
#compositeFramesInFolder("/Users/ckierum/LocalSync/production/assets/group_3/shot/seq_06_tada_0100/renders/5_05_2020_render/images/masterLayer")
#compositeFramesInFolder("/Users/ckierum/LocalSync/production/assets/group_3/shot/seq_06_tada_0100/renders/5_05_2020_v2_render/images/masterLayer")
#compositeFramesInFolder("/Users/ckierum/LocalSync/production/assets/group_3/shot/seq_06_tada_0100/renders/5_05_2020_v3_render/images/masterLayer")
#compositeFramesInFolder("/Users/ckierum/localSync/production/assets/group_2/shot/seq_05_pyramid_0600/renders/quickRenderTestTwoPlzDontFail/images")
compositeFramesInFolder("/Users/ckierum/localSync45/production/lighting/paths/ntThreeeThreeTwo/images/masterLayer")

'''
compositeFramesInFolder(shotsFolder + "/seq_01_intro_0100/final/images")
compositeFramesInFolder(shotsFolder + "/seq_01_intro_0200/final/images")
compositeFramesInFolder(shotsFolder + "/seq_01_intro_0300/final/images")
compositeFramesInFolder(shotsFolder + "/seq_01_intro_0400/final/images")
compositeFramesInFolder(shotsFolder + "/seq_01_intro_0500/final/images")
compositeFramesInFolder(shotsFolder + "/seq_02_cheese_0100/final/images")
compositeFramesInFolder(shotsFolder + "/seq_02_cheese_0200/final/images")
compositeFramesInFolder(shotsFolder + "/seq_02_cheese_0300/final/images")
# compositeFramesInFolder(shotsFolder + "/seq_03_sneak_out_0100/final/images")

compositeFramesInFolder(shotsFolder + "/seq_06_reunited_0400/final/images")
compositeFramesInFolder(shotsFolder + "/seq_03_sneak_out_0200/final/images")

compositeFramesInFolder(shotsFolder + "/seq_03_sneak_out_0300/final/images")
compositeFramesInFolder(shotsFolder + "/seq_04_panic_0100/final/images")
compositeFramesInFolder(shotsFolder + "/seq_05_search_0100/final/images")
compositeFramesInFolder(shotsFolder + "/seq_05_search_0200/final/images")
compositeFramesInFolder(shotsFolder + "/seq_05_search_0300/final/images")
compositeFramesInFolder(shotsFolder + "/seq_05_search_0400/final/images")
compositeFramesInFolder(shotsFolder + "/seq_05_search_0500/final/images")
compositeFramesInFolder(shotsFolder + "/seq_06_reunited_0100/final/images")
compositeFramesInFolder(shotsFolder + "/seq_06_reunited_0200/final/images")
compositeFramesInFolder(shotsFolder + "/seq_06_reunited_0300/final/images")
'''
#compositeFramesInFolder(shotsFolder + "/seq_06_reunited_0400/final/images")
#compositeFramesInFolder(shotsFolder + "/seq_07_end_0100/final/images")
#compositeFramesInFolder(shotsFolder + "/seq_07_end_0200/final/images")
#compositeFramesInFolder(shotsFolder + "/seq_07_end_0300/final/images")
#compositeFramesInFolder(shotsFolder + "/seq_07_end_0400/final/images")

#compositeFramesInFolder(shotsFolder + "/seq_01_intro_0400/rf/images")


#compositeFramesInFolder(shotsFolder + "/seq_01_intro_0300/rf3/images/")
#compositeFramesInFolder(shotsFolder + "/seq_06_reunited_0100/rf2/images/masterLayer")
#compositeFramesInFolder(shotsFolder + "/seq_01_intro_0400/rf3/images/")
#compositeFramesInFolder(shotsFolder + "/seq_01_intro_0300/rf2/images/")
#compositeFramesInFolder(shotsFolder + "/seq_01_intro_0400/rf2/images/")
#compositeFramesInFolder(shotsFolder + "/seq_05_search_0500/rf/images/masterLayer")
#compositeFramesInFolder(shotsFolder + "/seq_02_cheese_0200/rf/images/")
#compositeFramesInFolder(shotsFolder + "/seq_02_cheese_0100/rf/images/")
#compositeFramesInFolder(shotsFolder + "/seq_03_sneak_out_0200/rf/images/")
#compositeFramesInFolder(shotsFolder + "/seq_03_sneak_out_0300/rf/images/")
#compositeFramesInFolder(shotsFolder + "/seq_04_panic_0100/rf/images/")
#compositeFramesInFolder(shotsFolder + "/seq_05_search_0500/rf/images/masterLayer")

#compositeFramesInFolder(sshfsFolder + "/_student_files/yeoh_chin/cse459/project 9/calebBR/images")

#compositeFramesInFolder("/Users/ckierum/localSync/mousetrap/group06/asset/shots/seq_02_cheese_0300/br/images/masterLayer")