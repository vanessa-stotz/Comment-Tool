## This file is a modified version of Jon Maceys install.py script
## script original: ClutterBasePlugin from the ClutterBaseLab


import pathlib
import platform
import os
import sys
import subprocess

mayaLocations = {"Linux": "/maya/", "Windows": "/Documents/maya/"}


def installModules(mayaLoc, opSys):
    location = pathlib.Path(mayaLoc)
    createMod(location)
    moveShelfScript(location, opSys)


def createMod(location):
    currentDir = pathlib.Path.cwd()
    moduleDir = pathlib.Path.joinpath(location, "modules")
    modulePath = pathlib.Path.joinpath(moduleDir, "MayaCommentTool.mod")

    moduleDir.mkdir(exist_ok=True)

    if not pathlib.Path(modulePath).is_file():
        print("writing module file")
        with open(modulePath, "w") as file:
            file.write(f"+ MayaCommentTool 1.0 {currentDir}\n")
            file.write("MAYA_PLUG_IN_PATH +:= plugins\n")
            file.write("PYTHONPATH +:= python")
    print("module installed")


def moveShelfScript(location, opSys):
    currentDir = pathlib.Path.cwd()
    shelfDir = pathlib.Path.joinpath(currentDir, "installScripts")
    shelfFile = pathlib.Path.joinpath(shelfDir, "shelf_CommentTool.mel")
    locationShelfFile = pathlib.Path.joinpath(location, "2023/prefs")
    locationShelfFile = pathlib.Path.joinpath(locationShelfFile, "shelves")
    path = pathlib.Path(locationShelfFile)

    locationShelfFile.mkdir(exist_ok=True)

    if opSys == "Linux":
        command = f"cp {shelfFile} {locationShelfFile}"
        subprocess.run(command, shell=True)
    if opSys == "Windows":
        pathlib.WindowsPath(shelfFile)
        pathlib.WindowsPath(locationShelfFile)
        command = f"copy {shelfFile} {locationShelfFile}"
        subprocess.run(command, shell=True)
    print("shelf file copied")


def checkMayaInstalled(opSys):
    mayaLoc = f"{pathlib.Path.home()}{mayaLocations.get(opSys)}"
    if not os.path.isdir(mayaLoc):
        raise
    return mayaLoc


if __name__ == "__main__":

    try:
        opSys = platform.system()
        mayaLoc = checkMayaInstalled(opSys)
    except:
        print("Error can't find maya install")
        sys.exit(-1)
    installModules(mayaLoc, opSys)
