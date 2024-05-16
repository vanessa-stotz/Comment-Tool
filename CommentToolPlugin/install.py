import pathlib
import platform
import os
import sys
import subprocess

mayaLocations = {
        "Linux": "/maya/",
        "Windows": "/Documents/maya/"
}
def installModules(mayaLoc, opSys):
   location = pathlib.Path(mayaLoc)
   createMod(location)
   #moveShelfScript(location, opSys)
        

def createMod(location):
    currentDir = pathlib.Path.cwd()
    print(currentDir)
    moduleDir = pathlib.Path.joinpath(location, "modules")
    modulePath = pathlib.Path.joinpath(moduleDir, "test.mod")

    moduleDir.mkdir(exist_ok=True)

    if not pathlib.Path(modulePath).is_file():
        print("writing module file")
        with open(modulePath, "w") as file:
            file.write(f"+ <MayaEditor 1.0 {currentDir}\n")
            file.write("MAYA_PLUG_IN_PATH +:= plugins\n")
            file.write("PYTHONPATH +:= python")

def moveShelfScript(location, opSys) :
    currentDir = pathlib.Path.cwd()
    print(f"Current Dir {currentDir}")
    shelfDir = pathlib.Path.joinpath(currentDir, "installScripts")
    shelfFile = pathlib.Path.joinpath(shelfDir, "shelf_CommentTool.mel")
    print(shelfFile)
    locationShelfFile = pathlib.Path.joinpath(location, "2023/prefs/shelves" )
    locationShelfFile = pathlib.Path.joinpath(locationShelfFile, "shelf_CommentTool.mel")
    print(locationShelfFile)
    #if opSys == "Linux":
    #    subprocess.run(f"cp {str(shelfFile)} {str(locationShelfFile)}")
    # if opSys == 'Windows':
    #     subprocess.run(f"copy {str(shelfFile)} {str(locationShelfFile)}")


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