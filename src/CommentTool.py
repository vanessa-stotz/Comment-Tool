import json
#import jsonschema
#from jsonschema import validate


scene = {}

scene["sceneName"] = ""
scene["comments"] = []
#comment = {}

class CommentTool:

    def __init__(self, name : str) : 

        self.name = name


def writeJson(fileName):

    # with open('CommentToolSchema.json') as f:
    #     schema = json.load(f)

    # validate(instance=scene, schema=schema)

    with open(fileName, 'w') as f:
        json.dump(scene, f, indent=4)

def readJson(fileName):
    f = open(fileName)
    data = json.load(f)
    
    scene["sceneName"] = data['sceneName']
    scene["comments"] = data['comments']

    f.close()



def addCommentsToScene(frame, text) :

    comment = {}

    comment["frame"] = frame
    comment["text"] = text

    scene["comments"].append(comment)

    length = len(scene["comments"])
    content = scene["comments"]
    sortComments()


def sortComments():

    newList = sorted(scene["comments"], key = lambda x : x['frame'])
    scene["comments"] = newList

def getSceneDict():
    return scene

def deleteComment(index):
    scene["comments"].pop(index)

def clearScene():
    scene["comments"].clear()
