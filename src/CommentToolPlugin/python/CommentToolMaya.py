import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.OpenMayaUI as OpenMayaUI1
import maya.cmds as cmds
import importlib, pathlib
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.mel as mel

from shiboken2 import wrapInstance

from PySide2 import QtWidgets, QtGui, QtCore


# if (cmds.pluginInfo*'timeSliderBookmark', q = true, loaded = True) :
#     cmds.unloadPlugin('timeSliderBookmark')

cmds.loadPlugin('timeSliderBookmark')
import maya.plugin.timeSliderBookmark.timeSliderBookmark as bookmark
importlib.reload(bookmark)

import CommentTool
importlib.reload(CommentTool)

#from CommentTool import writeJson, readJson, addCommentsToScene, getSceneDict, deleteComment, clearScene


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
        
        self.rowCount = 0

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

    def resizeEvent(self,size):
        self.showTextTable.resizeRowsToContents()
        self.showTextTable.resizeColumnsToContents()

    def menuBar(self) :

        menu = QtWidgets.QMenuBar()
        menuFile = QtWidgets.QMenu("File")
        menuComments = QtWidgets.QMenu("Comments")
        actionExportBoth = QtWidgets.QAction("Export Comments and Video", self)
        actionExportComments = QtWidgets.QAction("Export Comments", self)
        actionExportVideo = QtWidgets.QAction("Export Video", self)
        actionImport = QtWidgets.QAction("Load Comments", self)
        actionClear = QtWidgets.QAction("Clear Comments", self)


        actionExportBoth.triggered.connect(self.exportComments)
        actionExportBoth.triggered.connect(self.exportVideo)
        actionExportComments.triggered.connect(self.exportComments)
        actionExportVideo.triggered.connect(self.exportVideo)
        actionImport.triggered.connect(self.importComments)
        actionClear.triggered.connect(self.clearComments)

        menuFile.addAction(actionExportBoth)
        menuFile.addAction(actionExportComments)
        menuFile.addAction(actionExportVideo)
        menuFile.addSeparator()
        menuFile.addAction(actionImport)

        menuComments.addAction(actionClear)

        menu.addMenu(menuFile)
        menu.addMenu(menuComments)
        self.gridLayout.addWidget(menu,0,0)

    def showTextLayout(self):
        showTextScrollArea = QtWidgets.QScrollArea()


        self.showTextTable = QtWidgets.QTableWidget()
        self.showTextTable.setColumnCount(4)
        self.showTextTable.setRowCount(self.rowCount)
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
        
        self.scene = CommentTool.getSceneDict()
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
        filePath = cmds.file(q=True, sn=True).rpartition('/')
        ##fileName = QtWidgets.QFileDialog.getSaveFileName(self, "Save JSON file", filePath[0], "JSON File (*.json)")
        ##if fileName[0] != "":
        CommentTool.writeJson(filePath)

    def exportVideo(self):
        filePath = cmds.file(q=True, sn=True).rpartition('/')
        
        #get the path to the comment Folder
        pathdir = CommentTool.getFolderPath(filePath[0])
        print(pathdir)
        name = filePath[2].rpartition('.')
        fileName = name[0] + ".mov"
        #show frame count
        mel.eval('setCurrentFrameVisibility(!`optionVar -q currentFrameVisibility`);')
        #hide framecount
        #export playblast
        cmds.playblast(format = "qt", filename = (str(pathdir) + fileName), fp = 4, percent =100, compression = "jpeg", quality = 100, width = 1920, height = 1080, fo=1, v = 0)
        print("video")
        mel.eval('setCurrentFrameVisibility(!`optionVar -q currentFrameVisibility`);')
        

    def importComments(self):
        filePath = cmds.file(q=True, sn=True).rpartition('/')
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Select JSON file", filePath[0], "JSON File (*.json)")
        if fileName[0] != "":
            CommentTool.readJson(fileName[0])
            self.displayText()
            self.addBookmarkToImport()


    def clearComments(self) :
        CommentTool.clearComments()
        self.clearBookmarks()
        self.displayText()



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
        self.scene  = CommentTool.getSceneDict()
        
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