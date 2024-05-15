#!/usr/bin/env python

import sys

from PySide2 import QtWidgets, QtGui, QtCore
import pathlib
import subprocess
import platform

import CommentTool
#from CommentTool import writeJson, readJson, addCommentsToScene, getSceneData, deleteComment, clearComments, exportCommentsFromStandalone

class CommentToolDialog(QtWidgets.QDialog):
    
    def __init__(self, parent = None) :
        
        #variables
        self.frame = 0
        self.text = ""
        self.scene = {}
        self.commentFilePath = ""

        self.scene["sceneName"] = ""
        self.scene["comments"] = []

        self.comment = {
                        "frame",
                        "comments"
                }
        
        self.rowCount = 0


        super(CommentToolDialog, self).__init__()
        self.setWindowTitle("Comment Tool")
        self.resize(800,800)

        #grid layout
        self.gridLayout = QtWidgets.QGridLayout()

        self.menuBar()

        # textfield
        self.showTextLayout()

        #input text
        self.inputTextLayout()

        #set Layout
        self.setLayout(self.gridLayout)

        length = len(self.scene["comments"])
        print(f"length  start {length}")


    def showEvent(self, event):
        self.loadVideofromStartUp()


    def closeEvent(self, event):
        print("closeEvent")
        self.closeVideo()

    def resizeEvent(self,size):
        print("resize")
        self.showTextTable.resizeRowsToContents()
        self.showTextTable.resizeColumnsToContents()

    def menuBar(self) :

        menu = QtWidgets.QMenuBar()
        menuFile = QtWidgets.QMenu("File")
        menuComments = QtWidgets.QMenu("Comments")
        menuVideo = QtWidgets.QMenu("Video")

        actionExport = QtWidgets.QAction("Save Comments", self)
        actionImport = QtWidgets.QAction("Load Comments", self)
        actionClear = QtWidgets.QAction("Clear Comments", self)

        actionOpenVideo = QtWidgets.QAction("Open Video", self)

        actionOpenVideo.triggered.connect(self.openVideo)
        actionExport.triggered.connect(self.exportComments)
        actionImport.triggered.connect(self.importComments)
        actionClear.triggered.connect(self.clearComments)

        
        menuFile.addAction(actionExport)
        menuFile.addAction(actionImport)
        menuComments.addAction(actionClear)
        menuVideo.addAction(actionOpenVideo)

        menu.addMenu(menuFile)
        menu.addMenu(menuVideo)
        menu.addMenu(menuComments)
        self.gridLayout.addWidget(menu, 0, 0)

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
        

        showTextScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        showTextScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        showTextScrollArea.setWidgetResizable(True)
        showTextScrollArea.setWidget(self.showTextTable)
        
        self.gridLayout.addWidget(showTextScrollArea, 1, 0)



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
        
        print("DisplayText")
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
        

    def openVideo(self):
        fielName = QtWidgets.QFileDialog.getOpenFileName(self, "Open Video", "./", "*.mov *.mp4")
        videoPath = str(fielName[0])
        if not videoPath == "":
            self.closeVideo()
            self.loadVideo(videoPath)
            self.loadCommentfromVideo(videoPath)
        

    #asks to open a video right at startup, can be cancelled
    def loadVideofromStartUp(self):

        loadVideoBox = QtWidgets.QMessageBox()
        loadVideoBox.setWindowTitle("Open Video")
        loadVideoBox.setText("Do you want to open a Video?")
        buttonYes = QtWidgets.QMessageBox.Yes
        buttonNo = QtWidgets.QMessageBox.No
        loadVideoBox.setStandardButtons(buttonYes|buttonNo)
        loadVideoBox.setDefaultButton(buttonNo)
        boxValue = loadVideoBox.exec_()
        if (boxValue == buttonYes):
            self.openVideo()


    # if there is a .json file inside of the video folder, this can be loaded aswell
    def loadCommentfromVideo(self, videoPath):
        file = videoPath.rpartition('.')
        print(file)
        self.commentFilePath = str(file[0]) + ".json"
        print(self.commentFilePath)
        if pathlib.Path(self.commentFilePath).exists():
            loadVideoBox = QtWidgets.QMessageBox()
            loadVideoBox.setText("Comments found")
            loadVideoBox.setInformativeText("Do you want to load them?")
            buttonYes = QtWidgets.QMessageBox.Yes
            buttonNo = QtWidgets.QMessageBox.No
            loadVideoBox.setStandardButtons(buttonYes|buttonNo)
            loadVideoBox.setDefaultButton(buttonYes)
            boxValue = loadVideoBox.exec_()
            if (boxValue == buttonYes):
                self.importComments()
        else :
            self.clearComments()


    #load the video in vlc
    def loadVideo(self, movPath):
        operationSystem = platform.system()
        process = QtCore.QProcess()
        filePath = pathlib.Path(movPath)
        print(filePath)
        if operationSystem == "Linux":
            process.startDetached(f"/usr/bin/vlc {str(movPath)}")
        if operationSystem == "Windows":
            process.setProgram("C:\\Program Files\\VideoLAN\\VLC\\vlc.exe")
            process.setArguments(f"{filePath}")
            process.startDetached()


    #kill the process of vlc after the main window is closed
    def closeVideo(self):
        operationSystem = platform.system()
        if operationSystem == "Linux":
            subprocess.run(["pkill", "vlc"])
        if operationSystem == "Windows":
            subprocess.run(["TASKKILL", "/IM", "VLC.EXE"])

    def addComment(self):

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
            print(self.frame)
            print(self.text)
            CommentTool.addCommentsToScene(self.frame, self.text)

            #clear input 
            self.inputText.clear()
            self.inputFrame.clear()
            

    #https://stackoverflow.com/questions/24148968/how-to-add-multiple-qpushbuttons-to-a-qtableview
    def deleteComment(self):
        button = self.sender()
        index = self.showTextTable.indexAt(button.pos())
        if index.isValid():
            print(index.row(), index.column())
            CommentTool.deleteComment(index.row())
            self.showTextTable.removeRow(index.row())


    def editComment(self):
        button = self.sender()
        index = self.showTextTable.indexAt(button.pos())
        if index.isValid():
            self.inputText.setText((self.scene['comments'][index.row()]['text']))
            self.inputFrame.setText(str(self.scene['comments'][index.row()]['frame']))
            CommentTool.deleteComment(index.row())
            self.showTextTable.removeRow(index.row())

            
    #endOfCitation

    def exportComments(self):
        print(self.commentFilePath)
        CommentTool.exportCommentsFromStandalone(self.commentFilePath)
        

    def importComments(self):
        print(self.commentFilePath)
        if not self.commentFilePath == "":
            CommentTool.readJson(self.commentFilePath)
            self.displayText()


    def clearComments(self) :
        print("Clear Comments")
        CommentTool.clearComments()
        self.displayText()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = CommentToolDialog()
    dialog.show()
    sys.exit(app.exec_())