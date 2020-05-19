import glob
import os 
from moviepy.editor import *
import subprocess

#sshfs -p 22 kieruc@attu.cs.washington.edu:/projects/instr/capstone4 ~/localSync
sshfsFolder = "/Users/ckierum/localSync4"
pathWithShots = "/production/assets/group_2/shot"
shotsFolder = sshfsFolder + pathWithShots

#shotsFolder = "/Users/ckierum/Coding/Animation Seminar Scripts/Testbed"
folderList = sorted(glob.glob(shotsFolder + "/*"))


shotLengthDict = {"seq_01_intro_0100"  : 235,
"seq_01_intro_0200"  : 161,
"seq_01_intro_0300"  : 181,
"seq_01_intro_0400"  : 66 ,
"seq_01_intro_0500"  : 38 ,
"seq_01_intro_0600"  : 173,
"seq_01_intro_0700"  : 65 ,
"seq_01_intro_0800"  : 38 ,
"seq_01_intro_0900"  : 57 ,
"seq_01_intro_1000"  : 44 ,
"seq_01_intro_1100"  : 66 ,
"seq_01_intro_1200"  : 75 ,
"seq_01_intro_1300"  : 66 ,
"seq_01_intro_1400"  : 35 ,
"seq_01_intro_1500"  : 34 ,
"seq_01_intro_1600"  : 56 ,
"seq_01_intro_1700"  : 42 ,
"seq_01_intro_1800"  : 37 ,
"seq_01_intro_1900"  : 39 ,
"seq_01_intro_2000"  : 68 ,
"seq_01_intro_2100"  : 34 ,
"seq_01_intro_2200"  : 54 ,
"seq_01_intro_2300"  : 67 ,
"seq_01_intro_2400"  : 45 ,
"seq_02_cube_0100"   : 44 ,
"seq_02_cube_0200"   : 73 ,
"seq_02_cube_0300"   : 37 ,
"seq_02_cube_0400"   : 62 ,
"seq_02_cube_0500"   : 52 ,
"seq_02_cube_0600"   : 169,
"seq_02_cube_0700"   : 151,
"seq_02_cube_0800"   : 56 ,
"seq_02_cube_0900"   : 74 ,
"seq_02_cube_1000"   : 136,
"seq_03_jump_0100"   : 143,
"seq_03_jump_0200"   : 72 ,
"seq_03_jump_0300"   : 44 ,
"seq_03_jump_0400"   : 61 ,
"seq_04_sphere_0100" : 95 ,
"seq_04_sphere_0200" : 88 ,
"seq_04_sphere_0300" : 60 ,
"seq_04_sphere_0400" : 76 ,
"seq_05_pyramid_0100": 101,
"seq_05_pyramid_0200": 32 ,
"seq_05_pyramid_0300": 26 ,
"seq_05_pyramid_0400": 28 ,
"seq_05_pyramid_0500": 33 ,
"seq_05_pyramid_0600": 72 ,
"seq_05_pyramid_0700": 48 ,
"seq_05_pyramid_0800": 48 ,
"seq_06_reverse_0100": 103,
"seq_06_reverse_0200": 54 ,
"seq_06_reverse_0300": 80 ,
"seq_06_reverse_0400": 114,
"seq_06_reverse_0500": 72 ,
"seq_06_reverse_0600": 57 ,
"seq_06_reverse_0700": 21 ,
"seq_06_reverse_0800": 38 ,
"seq_06_reverse_0900": 66 ,
"seq_06_reverse_1000": 109,
"seq_07_end_0100"    : 121,
"seq_07_end_0200"    : 84 ,
"seq_07_end_0300"    : 175}

hasVideo = []
videoPath = []
for folderpath in folderList:
    folder = folderpath[folderpath.rfind("/")+1:]
    print("Processing ", folder)
    filename = folder + ".avi"
    filepath = folderpath + "/" + filename
    print(filepath)
    if os.path.exists(filepath):
        print("Has video:", filepath)
        hasVideo.append(True)
        videoPath.append(folder)
    else:
        print("Does not have video...")
        hasVideo.append(False)
        videoPath.append(folder)
        
    print("")


w = 640
h = 360 # 16/9 screen
moviesize = w,h
moviefps = 24

finalDeleteList = []

finishedList = []
for i in range(len(hasVideo)):
    compositeArray = []
    folder = videoPath[i]
    fullPath = shotsFolder + "/" + folder + "/" + folder + ".avi"
    
    duration = 2
    print("Folder: ", folder, "fullPath:", fullPath)
    if (hasVideo[i] == True):
        print(fullPath)
        video = VideoFileClip(fullPath).fx(vfx.resize, width = w)
        print("Start Duration: ", video.duration)
        
        video = video.subclip(1, video.duration-1)
        compositeArray.append(video)
        duration = video.duration
        print("Duration: ", duration)
    else:
        duration = shotLengthDict[folder] / moviefps
        print("Getting duration from dictionary: ", duration)
        
        
        
    print("Generating video for ", videoPath[i])
    txt_clip = ( TextClip(folder,fontsize=30,color='white')
        .set_position(('right', 'bottom')).set_duration(duration))
    compositeArray.append(txt_clip)
    result = CompositeVideoClip(compositeArray, size=moviesize)
    createFileName = folder + ".mp4"
    result.write_videofile(createFileName, fps=moviefps)
    finishedList.append(createFileName)
    finalDeleteList.append(createFileName)

buildLongString = ""
for movie in finishedList:
    buildLongString += "file '" + movie + "'" + "\n"
    
f = open('shotList.txt', 'w')
f.write(buildLongString)
finalDeleteList.append("shotList.txt")

    
print("FFMPEG will create final video")
command = "ffmpeg -f concat -i shotList.txt -c copy merged.mp4"
print("Command we will run...", command)
#os.system(command)

    
#ffmpeg -i "concat:seq_01_intro_0100.mp4|seq_01_intro_0500.mp4" -c:a copy -c:v copy output.mp4

#ffmpeg -f concat -i shotList.txt -c copy merged.mp4
