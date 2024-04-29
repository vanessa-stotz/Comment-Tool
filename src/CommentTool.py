import json
from jsonschema import validate


scene = {}

scene["sceneName"] = ""
scene["comments"] = []
#comment = {}

class CommentTool:

    def __init__(self, name : str) : 

        self.name = name


def writeJson():

    print("writeJson")
    with open('CommentToolSchema.json') as f:
        schema = json.load(f)

    shot010 = {}

    shot010["sceneName"] = "shot 010"
    shot010["comments"] = []

    #add comments
    comments12 = {}
    comments12["frame"] = 12
    comments12["text"] = "Hello World"

    comments24 = {}
    comments24["frame"] = 24
    comments24["text"] = "Hello World 2"

    comments100 = {}
    comments100["frame"] = 100
    comments100["text"] = "sfhiugfhriug divdhgihgojbd vdif dughudrg bdasguidsfudhgirdhguvb f"


    shot010["comments"].append(comments12)
    shot010["comments"].append(comments24)
    shot010["comments"].append(comments100)

    validate(instance=scene, schema=schema)

    with open('scene.json', 'w') as f:
        json.dump(scene, f, indent=4)

    print("Written JSON")


def readJson():

    f = open('scene.json')
    data = json.load(f)

    print(f"Scene Name: {data['sceneName']}")

    comments = data['comments']

    print(" \nComments\n")
    for i in range (len(comments)):
        print(f"Frame: {comments[i]['frame']}")
        print(f"Text: \n    {comments[i]['text']}")

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
    return scene

def deleteComment(index):
    print("delete comment")
    scene["comments"].pop(index)
    ...
    
