import os
import sys

def renameFiles(filename, newname):
    os.rename(filename, newname)
    
if __name__ == '__main__':
    inputFolder = sys.argv[1]

    for root, dirs, files in os.walk(inputFolder):
        i=0
        for file in files:
            if file.endswith(".mp4"):
                print(os.path.join(root, file))
                renameFiles(os.path.join(root, file) , inputFolder + "" + str(i) + ".mp4")
                i+=1
