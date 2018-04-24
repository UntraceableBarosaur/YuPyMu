import os
import sys

branch      =   "UntraceableBarosaur/YuPyMu.git"
changedFilePath  = "gitTerm.py"

clone       =   "git clone https://github.com/"
clonePath   =   "/Users/Owen/Desktop"

pushpullPath  =  "/Users/Owen/Desktop/YuPyMu"
pull        =   "git pull https://github.com/"
add         =   "git add ."
commit      =   "git commit -am" + changedFilePath
push        =   "git push --all https://github.com/"

def gitPull(branch,pushpullPath):
    os.chdir(pushpullPath) # Specifying the path where the cloned project has to be copied
    try:
        os.system(pull+branch) # Pulling
    except RuntimeError:
        print("Pulling Failed")
    print("Pulling Successful")

def gitClone(branch,clonePath):
    os.chdir(clonePath) # Specifying the path where the cloned project has to be copied
    try:
        os.system(clone+branch) # Cloning
    except RuntimeError:
        print("Cloning Failed")
    print("Cloning Successful")

def gitPush(branch,pushpullPath):
    os.chdir(pushpullPath) # Specifying the path where the cloned project has to be copied
    try:
        os.system(add) # Adding
    except RuntimeError:
        print("Adding Failed")
    try:
        os.system(commit) # Commit the files
    except RuntimeError:
        print("Commiting Failed")
    try:
        os.system(push+branch) # Pushing
    except RuntimeError:
        print("Pushing Failed")
    print("Pushing Successful")
gitPush(branch,pushpullPath)
