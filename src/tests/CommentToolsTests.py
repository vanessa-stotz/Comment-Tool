import unittest
import sys
import jsonschema 
from jsonschema import validate
import json
from pathlib import Path

sys.path.append('..')

import CommentTool

scene = {}
scene["sceneName"] = ""
scene["comments"] = []

class TestCommentTool(unittest.TestCase):

    #check why json validate is not working
    def test_validateJson(self) :
        
        comment01 = {}
        comment01["frame"] = 23
        comment01["text"] = "Test Frame 23"

        comment02 = {}
        comment02["frame"] = 15
        comment02["text"] = "Test Frame 15"

        scene["comments"].append(comment01)
        scene["comments"].append(comment02)
        with open('../CommentToolSchema.json') as f:
            schema = json.load(f)
        
        validate(instance=scene,schema=schema)
        #print(validation)
        #self.assertTrue(validate(instance=scene,schema=schema))

        comment01 = {}
        comment01["frame"] = "23"
        comment01["text"] = 5

        comment02 = {}
        comment02["frame"] = "15"
        comment02["text"] = [0,2,2]

        scene["comments"].append(comment01)
        scene["comments"].append(comment02)
        with open('../CommentToolSchema.json') as f:
            schema = json.load(f)
        
        validate(instance=scene,schema=schema)
        #print(validation)
        #self.assertTrue(validate(instance=scene,schema=schema))




    def test_addAndSortComment(self):

        
        CommentTool.addComment(25, "TestFrame25")
        CommentTool.addComment(13,"TestFrame13")
        sceneTest = CommentTool.getSceneDict()

        #length of the comments should be 2 now
        self.assertEqual(2, len(sceneTest["comments"]))

        #test content of comments
        self.assertEqual(25, sceneTest["comments"][0]["frame"])
        self.assertEqual("TestFrame25", sceneTest["comments"][0]["text"])
        self.assertEqual(13, sceneTest["comments"][1]["frame"])
        self.assertEqual("TestFrame13", sceneTest["comments"][1]["text"])

        #order should have changed after sorting the comments
        #so order is different
        CommentTool.sortComments()
        sceneTest = CommentTool.getSceneDict()

        #shouldn't be equal
        self.assertNotEqual(25, sceneTest["comments"][0]["frame"])
        self.assertNotEqual("TestFrame25", sceneTest["comments"][0]["text"])
        self.assertNotEqual(13, sceneTest["comments"][1]["frame"])
        self.assertNotEqual("TestFrame13", sceneTest["comments"][1]["text"])

        #should be equal
        self.assertEqual(13, sceneTest["comments"][0]["frame"])
        self.assertEqual("TestFrame13", sceneTest["comments"][0]["text"])
        self.assertEqual(25, sceneTest["comments"][1]["frame"])
        self.assertEqual("TestFrame25", sceneTest["comments"][1]["text"])

        CommentTool.clearComments()



    def test_deleteComment(self):

        CommentTool.addCommentsToScene(25, "TestFrame25")
        CommentTool.addCommentsToScene(13,"TestFrame13")
        sceneTest = CommentTool.getSceneDict()

        #first test length of the comments
        self.assertEqual(2, len(sceneTest["comments"]))

        #delete comment at index 0 
        CommentTool.deleteComment(0)

        #length should be only one now
        self.assertEqual(1, len(sceneTest["comments"]))

        CommentTool.clearComments()



    def test_clearComments(self):

        CommentTool.addCommentsToScene(25, "TestFrame25")
        CommentTool.addCommentsToScene(13,"TestFrame13")
        sceneTest = CommentTool.getSceneDict()

        
        self.assertEqual(2, len(sceneTest["comments"]))

        CommentTool.clearComments()
        sceneTest = CommentTool.getSceneDict()

        self.assertEqual(0, len(sceneTest["comments"]))


    def test_overwriteComments(self):
        ...


    def test_writeAndReadFile(self):

        CommentTool.addCommentsToScene(4, "TestFrame4")
        CommentTool.addCommentsToScene(5,"Test5")

        #write Json File
        CommentTool.writeJson("testFile")

        path = Path("testFile.json")

        # check if file exists
        self.assertTrue(path.is_file())

        #read Json File
        CommentTool.readJson("testFile.json")
        sceneTest = CommentTool.getSceneDict()

        #test if the values are correct
        self.assertEqual("testFile.json", sceneTest["sceneName"])
        self.assertEqual(4, sceneTest["comments"][0]["frame"])
        self.assertEqual("TestFrame4", sceneTest["comments"][0]["text"])
        self.assertEqual(5, sceneTest["comments"][1]["frame"])
        self.assertEqual("Test5", sceneTest["comments"][1]["text"])

        CommentTool.clearComments()




if __name__ == '__main__':
    unittest.main()