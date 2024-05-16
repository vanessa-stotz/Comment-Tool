import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.OpenMayaUI as OpenMayaUI1
import maya.cmds as cmds
import importlib, pathlib
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.mel as mel
import os

from shiboken2 import wrapInstance

from PySide2 import QtWidgets, QtGui, QtCore
import src.CommentTool as CommentTool


def getMainWindow():
    window = OpenMayaUI1.MQtUtil.mainWindow()
    return wrapInstance(int(window),QtWidgets.QDialog)

class CommentToolDialog(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    
    def __init__(self, parent = getMainWindow()) :
        super(CommentToolDialog, self).__init__()

        #variables
        self.frame = 0
        self.text = ""
        self.scene = {}

        self.scene["sceneName"] = ""
        self.scene["comments"] = []

        self.comment = {
                        "frame",
                        "comments"
                }
        
        importlib.reload(CommentTool)

        self.idOpenScene = 0
        self.idNewScene = 0

        self.setWindowTitle("Comment Tool")
        self.resize(800,800)

        #grid layout
        self.gridLayout = QtWidgets.QGridLayout()

        #menubar
        self.menuBar()

        # textfield
        self.showTextLayout()

        # jumping between comments
        self.jumpFramesLayout()

        #input text
        self.inputTextLayout()

        #set Layout
        self.setLayout(self.gridLayout)

        #run scripts to reload after opening a new File or new scene
        self.scriptJobs()

    

    def scriptJobs(self):
        '''create jobs to either clear the comments when a new scene is opened
            or find comments if other scene is opened
        '''
        self.idOpenScene = cmds.scriptJob(event=["SceneOpened", self.findComments] )
        self.idNewScene = cmds.scriptJob(event=["NewSceneOpened", self.clearComments] )


    def showEvent(self, event):
        '''find comments after the tool is opened
        '''
        self.findComments()


    def hideEvent(self, event):
        ''' if tool is closed (only in hidden here, as it's a dockable window in maya)
            the existing script jobs are deleted to prevent the jobs from stacking up
        '''
        cmds.scriptJob( kill=self.idOpenScene, force=True )
        cmds.scriptJob( kill=self.idNewScene, force =True )


    def resizeEvent(self,size):
        '''resize the table if the window is resized
        '''
        self.showTextTable.resizeRowsToContents()
        self.showTextTable.resizeColumnsToContents()

    def menuBar(self) :
        '''creates the menuBar in the GUI
        '''
        menu = QtWidgets.QMenuBar()
        menuFile = QtWidgets.QMenu("File")
        menuComments = QtWidgets.QMenu("Comments")
        actionExportVideo = QtWidgets.QAction("Export Video", self)
        actionExportComments = QtWidgets.QAction("Export Comments", self)
        actionExportBoth = QtWidgets.QAction("Export Comments and Video", self)
        actionReload = QtWidgets.QAction("Reload Comments", self)
        actionClear = QtWidgets.QAction("Clear Comments", self)

        actionExportVideo.triggered.connect(self.exportVideo)
        actionExportComments.triggered.connect(self.exportComments)
        actionExportBoth.triggered.connect(self.exportComments)
        actionExportBoth.triggered.connect(self.exportVideo)
        actionReload.triggered.connect(self.reloadComments)
        actionClear.triggered.connect(self.clearComments)

        menuFile.addAction(actionExportVideo)
        menuFile.addAction(actionExportComments)
        menuFile.addAction(actionExportBoth)
        
        menuComments.addAction(actionReload)
        menuComments.addAction(actionClear)

        menu.addMenu(menuFile)
        menu.addMenu(menuComments)

        self.gridLayout.addWidget(menu,0,0)

    def showTextLayout(self):
        '''creates the Layout to show the comments in the GUI
        '''
        #create a scroll area to ensure a lot of comments can be created
        showTextScrollArea = QtWidgets.QScrollArea()
        # display of the comments is in a table
        self.showTextTable = QtWidgets.QTableWidget()
        self.showTextTable.setColumnCount(4)
        self.showTextTable.setRowCount(0)
        # table is 1. Frame, 2. Comments/Text, 3. button to edit the comment, 4. button to delete the comment
        self.showTextTable.setHorizontalHeaderLabels(["Frame", "Comment", "", ""])
        #resize the table
        self.showTextTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.showTextTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        # disable the function to edit the table
        self.showTextTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        # hide the index of the rows
        self.showTextTable.verticalHeader().setVisible(False)
        
        #activate to jump to frames while doubleclicking the according row
        self.showTextTable.clicked.connect(self.jumpToFrame)

        showTextScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        showTextScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        showTextScrollArea.setWidgetResizable(True)
        showTextScrollArea.setWidget(self.showTextTable)
        
        self.gridLayout.addWidget(showTextScrollArea, 1, 0)


    def jumpFramesLayout(self):
        '''layout to jump the frames of the comments
        '''
        jumpFramesGroup = QtWidgets.QGroupBox()
        jumpFramesLay = QtWidgets.QHBoxLayout()
        previousFrame = QtWidgets.QPushButton("|<")
        nextFrame = QtWidgets.QPushButton(">|")

        jumpFramesGroup.setLayout(jumpFramesLay)
        jumpFramesLay.addWidget(previousFrame)
        jumpFramesLay.addWidget(nextFrame)

        previousFrame.clicked.connect(self.jumpToPreviousFrame)
        nextFrame.clicked.connect(self.jumpToNextFrame)

        self.gridLayout.addWidget(jumpFramesGroup,2,0)


    def inputTextLayout(self):
        '''layout to write the comments
        '''
        inputTextGroup = QtWidgets.QGroupBox()
        inputTextLayout = QtWidgets.QVBoxLayout()
        inputFrameLayout = QtWidgets.QHBoxLayout()
        inputTextLayout.addLayout(inputFrameLayout)
        inputTextGroup.setLayout(inputTextLayout)

        inputFrameCheckBox = QtWidgets.QCheckBox()
        frameLabel = QtWidgets.QLabel("Frame")
        self.inputFrame = QtWidgets.QLineEdit()
        # allow the frame input to only accept integers
        self.inputFrame.setValidator(QtGui.QIntValidator(0,50000))
        
        # disable/enable the option to input a frame
        inputFrameCheckBox.setEnabled(True)
        self.inputFrame.setDisabled(True)
        inputFrameCheckBox.toggled.connect(self.inputFrame.setEnabled)

        self.inputText = QtWidgets.QTextEdit()
        addTextButton = QtWidgets.QPushButton("Add Comment")
        
        addTextButton.clicked.connect(self.addComment)
        addTextButton.clicked.connect(self.displayText)

        inputFrameLayout.addWidget(inputFrameCheckBox)
        inputFrameLayout.addWidget(frameLabel)
        inputFrameLayout.addWidget(self.inputFrame)
        inputTextLayout.addWidget(self.inputText)
        inputTextLayout.addWidget(addTextButton)

        self.gridLayout.addWidget(inputTextGroup, 3, 0)



    def displayText(self):
        '''displays the input comments to the showText layout
        '''
        self.scene = CommentTool.getSceneData()
        comments = self.scene['comments']
        #change the row count to the number of comments
        self.showTextTable.setRowCount(len(comments))

        #iterate over every comment and display it to the table
        for i in range (len(comments)) :
            frame = QtWidgets.QTableWidgetItem(f"{comments[i]['frame']}")
            text = QtWidgets.QTableWidgetItem(f"{comments[i]['text']}")
            delete = QtWidgets.QPushButton("delete")
            edit = QtWidgets.QPushButton("edit")

            self.showTextTable.setItem(i,0, frame)
            self.showTextTable.setItem(i,1, text)
            self.showTextTable.setCellWidget(i,2, edit)
            self.showTextTable.setCellWidget(i,3, delete)

            self.showTextTable.resizeColumnsToContents()
            self.showTextTable.resizeRowsToContents()

            delete.clicked.connect(self.deleteComment)
            edit.clicked.connect(self.editComment)
        


    def addComment(self):
        ''' add a comment to the directory, reads the input of the Text widgets of the GUI
        '''
        #get current frame in maya, so it doesn't jump if comment is written for another frame
        currentFrame = cmds.currentTime(query = True)
        #if no user input for frame == frame 0
        if not self.inputFrame.text() :
            self.frame = 0
        else :
            self.frame = int(self.inputFrame.text())

        #if no text is set, an error warning appears and process is aborted
        if not self.inputText.toPlainText() :
            error = QtWidgets.QMessageBox()
            error.warning(self, "Warning", "No input text. No comment added")

        #otherwise get the text from the inputText widget
        # and add the comments to the directory
        #delete the input frame and input text and set the frame to the one that was captured earlier
        else :
            self.text = self.inputText.toPlainText()
            CommentTool.addCommentsToScene(self.frame, self.text)
            #clear input 
            self.inputText.clear()
            self.inputFrame.clear()
            #set frame to the previous saved
            cmds.currentTime(currentFrame, edit = True)

    def deleteComment(self):
        ''' delete the comment in the row the button was clicked
        '''
        button = self.sender()
        index = self.showTextTable.indexAt(button.pos())
        # if the index exists delete the comment
        if index.isValid():
            CommentTool.deleteComment(index.row())
            self.showTextTable.removeRow(index.row())



    def editComment(self):
        '''edit the comment in the row the button was clicked
        '''
        button = self.sender()
        index = self.showTextTable.indexAt(button.pos())
        #to edit the the comment it gets deleted from the table and its content gets displayed in the input text layout
        if index.isValid():
            self.inputText.setText((self.scene['comments'][index.row()]['text']))
            self.inputFrame.setText(str(self.scene['comments'][index.row()]['frame']))
            CommentTool.deleteComment(index.row())
            self.showTextTable.removeRow(index.row())


    def exportComments(self):
        '''export the comments to a json file
        '''
        filePath = self.getFilePath()
        CommentTool.exportCommentsFromMayaAPI(filePath)

    def exportVideo(self):
        ''' export a playblast from the current scene
        '''
        #get the path to the folder of the maya scene
        filePath = self.getFilePath()
        #get the path of the personalised comment folder
        pathdir = CommentTool.getFolderPath(filePath)

        #get the root name of the file
        rootName = filePath[2].rpartition('.')
        fileName = rootName[0] + ".mov"
       
        pathVideo = pathlib.Path.joinpath(pathdir, fileName)
        #show frame count
        #only works if the frame count is currently hidden
        mel.eval('setCurrentFrameVisibility(!`optionVar -q currentFrameVisibility`);')
        #export playblast
        cmds.playblast(format = "qt", filename = str(pathVideo), fp = 4, percent =100, compression = "jpeg", quality = 100, width = 1920, height = 1080, fo=1, v = 0)
        #hide framecount
        mel.eval('setCurrentFrameVisibility(!`optionVar -q currentFrameVisibility`);')
        

    def findComments(self):
        '''looks in the folder path if a json file already exists and loads it if the user wants to
        '''
        filePath = self.getFilePath()
        #mayaFilePath = pathlib.Path(filePath[0])
        #mayaRoot = filePath[2].rpartition('.')
        folderDir = CommentTool.getFolderPath(filePath)
        # if the folder where the comments are expected exists list all the files and check for a json file
        if folderDir.is_dir():
            files = os.listdir(folderDir)
            for file in files:
                if file.endswith(".json"):
                    #change path to the json file
                    jsonDir = pathlib.Path.joinpath(folderDir, file)
                    # ask the user if the found comments should be loaded
                    loadJsonBox = QtWidgets.QMessageBox()
                    loadJsonBox.setWindowTitle("Comments found")
                    loadJsonBox.setText("Do you want to load them?")
                    buttonYes = QtWidgets.QMessageBox.Yes
                    buttonNo = QtWidgets.QMessageBox.No
                    loadJsonBox.setStandardButtons(buttonYes|buttonNo)
                    boxValue = loadJsonBox.exec_()
                    #if yes, they are loaded
                    if (boxValue == QtWidgets.QMessageBox.Yes):
                        self.loadComments(jsonDir)


    def getFilePath(self):
        '''export comments from standalone tool 
    
        Returns:
        list[]: returns the path, split in path to the file[0], partition / [1] and the file name [2]

        '''
        return cmds.file(q=True, sn=True).rpartition('/')        
        

    def reloadComments(self) :
        ''' basically the same function as the import comments, expect that it doesn't ask for consent from the user
            looks in the folder path if a json file already exists and loads it if the user wants to
        '''
        filePath = self.getFilePath()
        #mayaFilePath = pathlib.Path(filePath[0])
        #mayaRoot = filePath[2].rpartition('.')
        folderDir = CommentTool.getFolderPath(filePath)
        # if the folder where the comments are expected exists list all the files and check for a json file
        if folderDir.is_dir():
            files = os.listdir(folderDir)
            for file in files:
                if file.endswith(".json"):
                        jsonDir = pathlib.Path.joinpath(folderDir, file)
                        self.loadComments(jsonDir)



    def loadComments(self, jsonDir : str):
        ''' loads the json file into the scene and displays it in the showText Layout 
        
        Parameters:
        jsonDir (str): Path to the json file which should be loaded
        '''
        CommentTool.readJson(jsonDir)
        self.displayText()


    def clearComments(self) :
        '''clear data of the comments in directory 
        '''
        CommentTool.clearComments()
        self.displayText()

    
    #Maya specific functions

    def jumpToFrame(self):
        '''called if a row of the table is double clicked, if the index is a valid index
            it jumps to the displayed frame in that row
        '''
        for index in self.showTextTable.selectedIndexes():
            cmds.currentTime(self.scene['comments'][index.row()]['frame'], edit = True)

   
    def jumpToPreviousFrame(self):
        '''changes the current frame in maya to the previous frame of the comment
        '''
        #get the current frame
        currentFrame = cmds.currentTime(query = True)
        commentList = self.scene["comments"]
        #get the frame that is closest to current frame 
        closestComment = min(commentList, key = lambda x : abs(currentFrame - x['frame']))
        closestFrame = closestComment['frame']
        #and also the corresponding index
        indexClosestFrame = commentList.index(next(filter(lambda n :n.get('frame') == closestFrame, commentList)))

        # if the current Frame and the closest Frame are the same value it already is on that comment and should take the next smaller value
        # therefore get the index the closest frame and take the frame of the value -1
        if(currentFrame == closestFrame):
            # if the index is zero, the smallest index is already displaying, therefore got to the end of the comments list and take this as the current frame
            if(indexClosestFrame == 0):
                length = len(commentList)
                previousComment = commentList[length -1]
                closestFrame= previousComment['frame']
            else :
                previousComment = commentList[indexClosestFrame-1]
                closestFrame = previousComment['frame']

        # as the closest value could also be greater than the current frame, the code has to check for that
        # and takes the frame value of the previous index
        elif(currentFrame < closestFrame):
            previousComment = commentList[indexClosestFrame-1]
            closestFrame = previousComment['frame']

        # update the currentTime to the closest frame that has been found
        cmds.currentTime(closestFrame, edit = True)

    def jumpToNextFrame(self):
        '''changes the current frame in maya to the next frame of the comment
        '''
        #get the current frame
        currentFrame = cmds.currentTime(query = True)
        commentList = self.scene["comments"]
        #get the frame that is closest to current frame 
        closestComment = min(commentList, key = lambda x : abs(currentFrame - x['frame']))
        closestFrame = closestComment['frame']
        #and also the corresponding index
        indexClosestFrame = commentList.index(next(filter(lambda n :n.get('frame') == closestFrame, commentList)))

        # if the current Frame and the closest Frame are the same value it already is on that comment and should take the next bigger value
        # therefore get the index the closest frame and take the frame of the value +1
        if(currentFrame == closestFrame):
            length = len(commentList)
            # if the index is the last in the list, the biggest index is already displaying, therefore got to the beginning of the comments list and take this as the current frame
            if(indexClosestFrame == length-1):
                nextComment = commentList[0]
                closestFrame= nextComment['frame']
            else :
                nextComment = commentList[indexClosestFrame+1]
                closestFrame = nextComment['frame']

        # as the closest value could also be smaller than the current frame, the code has to check for that
        # and takes the frame value of the next index
        elif(currentFrame > closestFrame):
            nextComment = commentList[indexClosestFrame+1]
            closestFrame = nextComment['frame']

        cmds.currentTime(closestFrame, edit = True)





if __name__ == "__main__":
    try:
       commentToolDialog.close()
       commentToolDialog.deleteLater()
    except:
       pass
   
    commentToolDialog = CommentToolDialog()
    commentToolDialog.show()