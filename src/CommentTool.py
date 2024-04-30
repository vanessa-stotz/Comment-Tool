import json
from jsonschema import validate


scene = {}

scene["sceneName"] = ""
scene["comments"] = []
#comment = {}

class CommentTool:

    def __init__(self, name : str) : 

        self.name = name


def writeJson(fileName):

    print("writeJson")
    with open('CommentToolSchema.json') as f:
        schema = json.load(f)

    validate(instance=scene, schema=schema)

    with open(fileName, 'w') as f:
        json.dump(scene, f, indent=4)

    print("Written JSON")


def readJson(fileName):
    print(fileName)
    f = open(fileName)
    data = json.load(f)
    
    scene["sceneName"] = data['sceneName']
    scene["comments"] = data['comments']

    f.close()



def addCommentsToScene(frame, text) :

    comment = {}

    print(frame)
    print(text)

    comment["frame"] = frame
    comment["text"] = text

    scene["comments"].append(comment)

    length = len(scene["comments"])
    print(f"length update {length}")
    content = scene["comments"]
    print(f"content {content}")
    print(comment)
    sortComments()


def sortComments():

    print("sorted comments")
    newList = sorted(scene["comments"], key = lambda x : x['frame'])
    scene["comments"] = newList
    print(scene["comments"])

def getSceneDict():
    print("get scene")
    print(scene)
    return scene

def deleteComment(index):
    print("delete comment")
    scene["comments"].pop(index)

def clearScene():
    scene["comments"].clear()
