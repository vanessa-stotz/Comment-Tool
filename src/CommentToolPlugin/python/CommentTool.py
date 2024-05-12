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


def writeJson(path : str):

    pathDir = createFolder(path[0])
    name = path[2].rpartition('.')
    fileName = name[0] + ".json"
    scene["sceneName"] = path[2]
    # with open('CommentToolSchema.json') as f:
    #     schema = json.load(f)

    # validate(instance=scene, schema=schema)
    with open(pathlib.Path.joinpath(pathDir, fileName), 'w') as f:
        json.dump(scene, f, indent=4)



def getFolderPath(path):
    pathNew = pathlib.Path(path)
    pathDir = pathlib.Path.joinpath(pathNew, "Comments")

    if pathDir.is_dir():
        print("Folder exists")
    else:
        print("createFolder")
        os.mkdir(pathDir)
    return pathDir
    

def readJson(fileName : str):
    f = open(fileName)
    data = json.load(f)

    overwriteComments(data) 

    f.close()


def addComment(frame : int, text : str) :

    comment = {}

    comment["frame"] = frame
    comment["text"] = text

    scene["comments"].append(comment)

    #length = len(scene["comments"])
    #content = scene["comments"]

def addCommentsToScene(frame : int, text : str) :
    
    addComment(frame, text)
    sortComments()


def sortComments():
    newList = sorted(scene["comments"], key = lambda x : x['frame'])
    scene["comments"] = newList

def getSceneDict():
    return scene

def overwriteComments(data : dict):
    scene["sceneName"] = data['sceneName']
    scene["comments"] = data['comments']

def deleteComment(index : int):
    scene["comments"].pop(index)

def clearComments():
    scene["comments"].clear()

