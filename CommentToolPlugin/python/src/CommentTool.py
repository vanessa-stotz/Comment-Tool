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

def exportCommentsFromStandalone(path : str):
    
    '''export comments from standalone tool 
    
    Parameters: 
    path (str): path to the json File thats going to be created
    
    '''

    jsonName = path.rpartition('/')
    rootName = jsonName[2].rpartition('.')
    #set sceneName as rootName
    setSceneName(rootName[0])
    
    writeJson(path)


def exportCommentsFromMayaAPI(path : list):

    '''export comments from maya plugin 
    
    Parameters: 
    path (str): path to the maya file in a list writing (path, /, filename)
    
    '''
    #get the path to the folder where the comments are saved
    pathDir = getFolderPath(path)

    #set the sceneName and json File name to the maya scene name without .ma extension
    rootName = path[2].rpartition('.')
    jsonFileName = rootName[0] + ".json"
    setSceneName(rootName[0])
    #write json File
    jsonPath = pathlib.Path.joinpath(pathDir, jsonFileName)
    writeJson(jsonPath)


def writeJson(path : str):
    '''write json file to path 
    
    Parameters: 
    path (str): path where the json file is being saved
    
    '''
    with open(path, 'w') as f:
        json.dump(scene, f, indent=4)

def getFolderPath(path: list):
    '''check if the folder where the video and json file is being saved exists, if not create them.
        first Folder is created inside the same folder as the maya file and named Comments
        the second folder is created inside the Comments Folder and named after the maya file(without the extension)
        inside this folder the json and video is saved 
    
    Parameters: 
    path (list): path where the json file is being saved
    
    Returns:
    string: path to the folder that either already exists or was created
    '''
    pathToMayaFile = pathlib.Path(path[0])
    #create a new path to the comments folder
    pathDirComments = pathlib.Path.joinpath(pathToMayaFile, "Comments")
    
    # if that path is not a directory, create it 
    if not pathDirComments.is_dir():
        os.mkdir(pathDirComments)

    # create new path to folder with maya scene name
    rootName = path[2].rpartition(".")
    pathDirNameFolder = pathlib.Path.joinpath(pathDirComments, rootName[0])

    # if that path is not a directory, create it 
    if not pathDirNameFolder.is_dir():
        os.mkdir(pathDirNameFolder)

    #return that path
    return pathDirNameFolder
    

def readJson(jsonDir : str):
    '''read an existing python file 
    
    Parameters: 
    jsonDir (str): path to the existing json file
    
    Returns:
    string: path to the folder that either already exists or was created
    '''
    f = open(jsonDir)
    data = json.load(f)

    #overwrite the existing directory with the new one
    overwriteComments(data) 

    f.close()

def addCommentsToScene(frame : int, text : str) :
    '''add a comment to the directory and sort all the comments
    
    Parameters: 
    frame (int): frame number in integer
    text (str): text corresponding to the frame
    '''
    
    #add the comment
    addComment(frame, text)
    #sort the comments
    sortComments()

def addComment(frame : int, text : str) :
    '''add a comment to the directory
    
    Parameters: 
    frame (int): frame number in integer
    text (str): text corresponding to the frame
    '''
    comment = {}

    comment['frame'] = frame
    comment['text'] = text

    scene["comments"].append(comment)


def sortComments():
    '''sort all the comments with the frame as key
    '''
    newList = sorted(scene["comments"], key = lambda x : x['frame'])
    scene["comments"] = newList


def getSceneData():
    '''get the current data of the directory
    '''
    return scene

def overwriteComments(data : dict):
    '''overrite the current directory with new 

    Parameters:
    data (dict): a new directory to overwrite the current
    '''
    scene["sceneName"] = data['sceneName']
    scene["comments"] = data['comments']

def deleteComment(index : int):
    '''delete a comment at index

    Parameters:
    index (int): index of the comment that is deleted
    '''
    scene["comments"].pop(index)

def clearComments():
    '''clear data of the comments in directory
    '''
    scene["comments"].clear()

def setSceneName(name :str):
     '''set the sceneName of the directory 

    Parameters:
    name (str): name the scene should have
    '''
     scene["sceneName"] = name