import json
import os
import pathlib
#import jsonschema
#from jsonschema import validate


scene = {}

scene["sceneName"] = ""
scene["comments"] = []

class CommentTool:

    def __init__(self, name : str) : 

        self.name = name


def exportCommentsFromStandalone(path :str):
    print(path)
    jsonName = path.rpartition('/')
    rootName = jsonName[2].rpartition('.')
    setSceneName(rootName[0])
    writeJson(path)


def exportCommentsFromMayaAPI(path):
    print("MayaPath")
    print(path)
    pathDir = getFolderPath(path)
    name = path[2].rpartition('.')
    fileName = name[0] + ".json"
    setSceneName(name[0])
    jsonPath = pathlib.Path.joinpath(pathDir, fileName)
    writeJson(jsonPath)


def writeJson(path : str):
    print("writeJson")
    print(path)
    with open(path, 'w') as f:
        json.dump(scene, f, indent=4)

def getFolderPath(path):
    print("Folder Path")
    print(path)
    pathNew = pathlib.Path(path[0])
    print(pathNew)
    pathDir = pathlib.Path.joinpath(pathNew, "Comments")
    nameFolder = path[2].rpartition(".")
    print(nameFolder)
    nameFolderDir = pathlib.Path.joinpath(pathDir, nameFolder[0])
    print(pathDir)

    if pathDir.is_dir():
        print("Folder exists")
    else:
        print("createFolder")
        os.mkdir(pathDir)
    
    if not nameFolderDir.is_dir():
        os.mkdir(nameFolderDir)

    return nameFolderDir
    

def readJson(fileName : str):
    print("readJson")
    f = open(fileName)
    data = json.load(f)

    overwriteComments(data) 

    f.close()

def addCommentsToScene(frame : int, text : str) :
    
    addComment(frame, text)
    sortComments()

def addComment(frame : int, text : str) :

    comment = {}

    comment["frame"] = frame
    comment["text"] = text

    scene["comments"].append(comment)

    #length = len(scene["comments"])
    #content = scene["comments"]


def sortComments():
    newList = sorted(scene["comments"], key = lambda x : x['frame'])
    scene["comments"] = newList

def getSceneData():
    return scene

def overwriteComments(data : dict):
    scene["sceneName"] = data['sceneName']
    scene["comments"] = data['comments']

def deleteComment(index : int):
    scene["comments"].pop(index)

def clearComments():
    scene["comments"].clear()

def setSceneName(name :str):
     scene["sceneName"] = name