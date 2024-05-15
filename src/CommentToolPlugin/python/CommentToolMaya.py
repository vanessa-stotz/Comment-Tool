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


if (cmds.pluginInfo('timeSliderBookmark', q = True, loaded = True)) :
     cmds.unloadPlugin('timeSliderBookmark')

cmds.loadPlugin('timeSliderBookmark')
import maya.plugin.timeSliderBookmark.timeSliderBookmark as bookmark
importlib.reload(bookmark)

import CommentTool
importlib.reload(CommentTool)

#from CommentTool import writeJson, readJson, addCommentsToScene, getSceneData, deleteComment, clearScene


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
        
        #self.jsonDir  = ""


        importlib.reload(bookmark)
        importlib.reload(CommentTool)

        #super(CommentToolDialog, self).__init__()
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

        length = len(self.scene["comments"])

        #readJson()
        #writeJson()

    def closeEvent(self, event):
        print("close")
        self.clearBookmarks()

    def showEvent(self, event):
        print("open")
        self.findComments()

    def resizeEvent(self,size):
        self.showTextTable.resizeRowsToContents()
        self.showTextTable.resizeColumnsToContents()

    def menuBar(self) :

        menu = QtWidgets.QMenuBar()
        menuFile = QtWidgets.QMenu("File")
        menuComments = QtWidgets.QMenu("Comments")
        menuExternal = QtWidgets.QMenu("External")
        actionExportVideo = QtWidgets.QAction("Export Video", self)
        actionExportComments = QtWidgets.QAction("Export Comments", self)
        actionExportBoth = QtWidgets.QAction("Export Comments and Video", self)
        actionReload = QtWidgets.QAction("Reload Comments", self)
        actionClear = QtWidgets.QAction("Clear Comments", self)
        actionExternal = QtWidgets.QAction("Open External Program", self)

        actionExportBoth.triggered.connect(self.exportComments)
        actionExportBoth.triggered.connect(self.exportVideo)
        actionExportComments.triggered.connect(self.exportComments)
        actionExportVideo.triggered.connect(self.exportVideo)
        actionReload.triggered.connect(self.reloadComments)
        actionClear.triggered.connect(self.clearComments)
        actionExternal.triggered.connect(self.openExternal)

        menuFile.addAction(actionExportVideo)
        menuFile.addAction(actionExportComments)
        menuFile.addAction(actionExportBoth)
        
        menuComments.addAction(actionReload)
        menuComments.addAction(actionClear)

        menuExternal.addAction(actionExternal)

        menu.addMenu(menuFile)
        menu.addMenu(menuComments)
        menu.addMenu(menuExternal)
        self.gridLayout.addWidget(menu,0,0)

    def showTextLayout(self):
        showTextScrollArea = QtWidgets.QScrollArea()


        self.showTextTable = QtWidgets.QTableWidget()
        self.showTextTable.setColumnCount(4)
        self.showTextTable.setRowCount(0)
        self.showTextTable.setHorizontalHeaderLabels(["Frame", "Comment", "", ""])
        self.showTextTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.showTextTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.showTextTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.showTextTable.verticalHeader().setVisible(False)
        
        self.showTextTable.clicked.connect(self.jumpToFrame)

        showTextScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        showTextScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        showTextScrollArea.setWidgetResizable(True)
        showTextScrollArea.setWidget(self.showTextTable)
        
        self.gridLayout.addWidget(showTextScrollArea, 1, 0)


    def jumpFramesLayout(self):

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
        inputTextGroup = QtWidgets.QGroupBox()
        inputTextLayout = QtWidgets.QVBoxLayout()

        
        inputFrameLayout = QtWidgets.QHBoxLayout()
        inputTextLayout.addLayout(inputFrameLayout)
        inputTextGroup.setLayout(inputTextLayout)

        inputFrameCheckBox = QtWidgets.QCheckBox()
        frameLabel = QtWidgets.QLabel("Frame")
        self.inputFrame = QtWidgets.QLineEdit()
        self.inputFrame.setValidator(QtGui.QIntValidator(0,50000))
        
        inputFrameCheckBox.setEnabled(True)
        self.inputFrame.setDisabled(True)
        inputFrameCheckBox.toggled.connect(self.inputFrame.setEnabled)
        
        inputFrameLayout.addWidget(inputFrameCheckBox)
        inputFrameLayout.addWidget(frameLabel)
        inputFrameLayout.addWidget(self.inputFrame)


        
        self.inputText = QtWidgets.QTextEdit()
        addTextButton = QtWidgets.QPushButton("Add Comment")
        inputTextLayout.addWidget(self.inputText)
        inputTextLayout.addWidget(addTextButton)
        addTextButton.clicked.connect(self.addComment)
        addTextButton.clicked.connect(self.displayText)

        self.gridLayout.addWidget(inputTextGroup, 3, 0)



    def displayText(self):
        print("displayText")
        self.scene = CommentTool.getSceneData()
        comments = self.scene['comments']
        self.showTextTable.setRowCount(len(comments))



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
        #get current frame in maya, so it doesn't jump if comment is written for another comment
        currentFrame = cmds.currentTime(query = True)
        #if no user input for frame == frame 0
        if not self.inputFrame.text() :
            self.frame = 0
        else :
            self.frame = int(self.inputFrame.text())

        if not self.inputText.toPlainText() :
            error = QtWidgets.QMessageBox()
            error.warning(self, "Warning", "No input text. No comment added")

        else :
            self.text = self.inputText.toPlainText()
            CommentTool.addCommentsToScene(self.frame, self.text)

            self.addBookmark(self.frame)
            #clear input 
            self.inputText.clear()
            self.inputFrame.clear()
            cmds.currentTime(currentFrame, edit = True)
        

    #https://stackoverflow.com/questions/24148968/how-to-add-multiple-qpushbuttons-to-a-qtableview
    def deleteComment(self):
        button = self.sender()
        index = self.showTextTable.indexAt(button.pos())
        if index.isValid():
            self.deleteBookmark(self.scene['comments'][index.row()]['frame'])
            CommentTool.deleteComment(index.row())
            self.showTextTable.removeRow(index.row())



    def editComment(self):
        button = self.sender()
        index = self.showTextTable.indexAt(button.pos())
        if index.isValid():
            self.inputText.setText((self.scene['comments'][index.row()]['text']))
            self.inputFrame.setText(str(self.scene['comments'][index.row()]['frame']))
            self.deleteBookmark(self.scene['comments'][index.row()]['frame'])
            CommentTool.deleteComment(index.row())
            self.showTextTable.removeRow(index.row())

            
    #endOfCitation

    def exportComments(self):
        filePath = self.getFilePath()
        print(filePath)
        #fileName = QtWidgets.QFileDialog.getSaveFileName(self, "Save JSON file", filePath[0], "JSON File (*.json)")
        #if fileName[0] != "":
        CommentTool.exportCommentsFromMayaAPI(filePath)

    def exportVideo(self):
        #get the path to the folder of the maya scene
        filePath = self.getFilePath()
        print(filePath)
        #get the path of the comment folder
        pathdir = CommentTool.getFolderPath(filePath)
        print("PathDir")
        print(pathdir)
        name = filePath[2].rpartition('.')
        fileName = name[0] + ".mov"
        #show frame count
        fileNew = pathlib.Path.joinpath(pathdir, fileName)
        mel.eval('setCurrentFrameVisibility(!`optionVar -q currentFrameVisibility`);')
        #hide framecount
        #export playblast
        cmds.playblast(format = "qt", filename = str(fileNew), fp = 4, percent =100, compression = "jpeg", quality = 100, width = 1920, height = 1080, fo=1, v = 0)
        print("video")
        mel.eval('setCurrentFrameVisibility(!`optionVar -q currentFrameVisibility`);')
        

    def findComments(self):
        print("findComments")
        filePath = self.getFilePath()
        mayaFilePath = pathlib.Path(filePath[0])
        print(mayaFilePath)
        mayaRoot = filePath[2].rpartition('.')
        print(mayaRoot[0])
        folderDir = pathlib.Path.joinpath(mayaFilePath, "Comments")
        print(folderDir)
        if folderDir.is_dir():
            folderDir = pathlib.Path.joinpath(folderDir, mayaRoot[0])
            print(folderDir)   
            if folderDir.is_dir():
                print("Folder exists")
                files = os.listdir(folderDir)
                print(files)
                print(len(files))
                for file in files:
                    if file.endswith(".json"):
                        print("is json")
                        jsonDir = pathlib.Path.joinpath(folderDir, file)
                        print(jsonDir)
                        print("same sceneName")
                        loadJsonBox = QtWidgets.QMessageBox()
                        loadJsonBox.setWindowTitle("Comments found")
                        loadJsonBox.setText("Do you want to load them?")
                        buttonYes = QtWidgets.QMessageBox.Yes
                        buttonNo = QtWidgets.QMessageBox.No
                        loadJsonBox.setStandardButtons(buttonYes|buttonNo)
                        boxValue = loadJsonBox.exec_()
                        if (boxValue == QtWidgets.QMessageBox.Yes):
                            print("load JSon")
                            self.importComments(jsonDir)
        #                 else :
        #                     print("no")
        #             else :
        #                 ("false")

    def getFilePath(self):
        return cmds.file(q=True, sn=True).rpartition('/')        
        

    def reloadComments(self) :
        print("findComments")
        filePath = self.getFilePath()
        mayaFilePath = pathlib.Path(filePath[0])
        print(mayaFilePath)
        mayaRoot = filePath[2].rpartition('.')
        print(mayaRoot[0])
        folderDir = pathlib.Path.joinpath(mayaFilePath, "Comments")
        print(folderDir)
        if folderDir.is_dir():
            folderDir = pathlib.Path.joinpath(folderDir, mayaRoot[0])
            print(folderDir)   
            if folderDir.is_dir():
                print("Folder exists")
                files = os.listdir(folderDir)
                print(files)
                print(len(files))
                for file in files:
                    if file.endswith(".json"):
                        jsonDir = pathlib.Path.joinpath(folderDir, file)
                        self.importComments(jsonDir)
            else:
                error = QtWidgets.QMessageBox()
                error.warning(self, "Warning", "No Comments found")
                self.clearComments()
        else:
                error = QtWidgets.QMessageBox()
                error.warning(self, "Warning", "No Comments found")
                self.clearComments()



    def importComments(self, jsonDir):
        print(jsonDir)
        CommentTool.readJson(jsonDir)
        self.displayText()
        #maya keeps crashing because of that ->
        #self.addBookmarkToImport()


    def clearComments(self) :
        CommentTool.clearComments()
        self.clearBookmarks()
        self.displayText()

    def openExternal(self):
        process = QtCore.QProcess()
        # how to do that ???
        process.startDetached(f"/home/s5602665/PipTD/msccavepipelineandtdproject24-vanessa-stotz/src/dist/CommentToolExec/CommentToolExec")

    #Maya specific functions

    def addBookmark(self, frame):
        print("add Bookmark")
        bookmark.createBookmark(name = f"Comment_{frame}", start = frame, stop = frame, color = (0,1,0))
        
    def deleteBookmark(self, frame) :
        bookmark.deleteBookmarkAtTime(time = frame)

    def clearBookmarks(self):
        print("delete bookmarks")
        bookmark.deleteAllBookmark()

    def addBookmarkToImport(self) :
        self.clearBookmarks()
        self.scene  = CommentTool.getSceneData()
        
        for comments in self.scene['comments'] :
            print(comments['frame'])
            self.addBookmark(comments['frame'])

    def jumpToFrame(self):

        for index in self.showTextTable.selectedIndexes():
            print(index.row())
            cmds.currentTime(self.scene['comments'][index.row()]['frame'], edit = True)

    def jumpToPreviousFrame(self):
        currentTime = cmds.currentTime(query = True)
        print("previous frame")
        print(bookmark.selectPreviousBookmarkAtTime(time = currentTime))

    def jumpToNextFrame(self):
        currentTime = cmds.currentTime(query = True)
        print("next frame")
        print(bookmark.selectNextBookmarkAtTime(time = currentTime))


if __name__ == "__main__":
    try:
       commentToolDialog.close()
       commentToolDialog.deleteLater()
    except:
       pass
   
    commentToolDialog = CommentToolDialog()
    commentToolDialog.show()