#!/usr/bin/env python

import sys
import os

from PySide2 import QtWidgets, QtGui, QtCore
import pathlib
import subprocess

from CommentTool import writeJson, readJson, addCommentsToScene, getSceneDict, deleteComment, clearComments


class CommentToolDialog(QtWidgets.QDialog):
    
    def __init__(self, parent = None) :
        
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
        menu.addMenu(menuComments)
        menu.addMenu(menuVideo)
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
        self.scene = getSceneDict()
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
        print("open VLC")
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Save JSON file", "./", "*.mov *.mp4")
        #CommentToolVideo.openVideo(fileName)
        file = str(fileName[0])
        self.loadVideo(file)
        

    def loadVideofromStartUp(self, path):
        filePath = path.rpartition('.')
        print(filePath)
        movPath = str(filePath[0]) + ".mov"
        if pathlib.Path(movPath).exists():
    
            loadJsonBox = QtWidgets.QMessageBox()
            loadJsonBox.setText("Video found")
            loadJsonBox.setInformativeText("Do you want to load it?")
            buttonYes = QtWidgets.QMessageBox.Yes
            buttonNo = QtWidgets.QMessageBox.No
            loadJsonBox.setStandardButtons(buttonYes|buttonNo)
            boxValue = loadJsonBox.exec_()
            if (boxValue == buttonYes):
                self.loadVideo(movPath)


    def loadVideo(self, movPath):
        process = QtCore.QProcess()
        filePath = str(movPath)
        print(filePath)
        process.startDetached(f"/usr/bin/vlc {str(movPath)}")


    def closeVideo(self):
        subprocess.run(["pkill", "vlc"])

    def addComment(self):

        print("new Comment")
        
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
            addCommentsToScene(self.frame, self.text)

        
            #clear input 
            self.inputText.clear()
            self.inputFrame.clear()
            

        


    #https://stackoverflow.com/questions/24148968/how-to-add-multiple-qpushbuttons-to-a-qtableview
    def deleteComment(self):
        button = self.sender()
        index = self.showTextTable.indexAt(button.pos())
        if index.isValid():
            print(index.row(), index.column())
            deleteComment(index.row())
            self.showTextTable.removeRow(index.row())


    def editComment(self):
        button = self.sender()
        index = self.showTextTable.indexAt(button.pos())
        if index.isValid():
            self.inputText.setText((self.scene['comments'][index.row()]['text']))
            self.inputFrame.setText(str(self.scene['comments'][index.row()]['frame']))
            deleteComment(index.row())
            self.showTextTable.removeRow(index.row())

            
    #endOfCitation

    def exportComments(self):
        fileName = QtWidgets.QFileDialog.getSaveFileName(self, "Save JSON file", "./", "JSON File (*.json)")
        if fileName[0] != "":
            writeJson(fileName[0])
        
        
        

    def importComments(self):
        print("Import Comments")
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Select JSON file", "./", "JSON File (*.json)")
        print(fileName)
        neName = str(fileName[0])
        if fileName[0] != "":
            readJson(fileName[0])
            self.displayText()
        self.loadVideofromStartUp(neName)


    def clearComments(self) :
        print("Clear Comments")
        clearComments()
        self.displayText()