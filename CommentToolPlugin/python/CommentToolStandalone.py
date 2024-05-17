#!/usr/bin/env python

import sys

from PySide2 import QtWidgets, QtGui, QtCore
import pathlib
import subprocess
import platform

import CommentTool

# from CommentTool import writeJson, readJson, addCommentsToScene, getSceneData, deleteComment, clearComments, exportCommentsFromStandalone


class CommentToolDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):

        # variables
        self.frame = 0
        self.text = ""
        self.scene = {}
        self.commentFilePath = ""

        self.scene["sceneName"] = ""
        self.scene["comments"] = []

        self.comment = {"frame", "comments"}

        self.rowCount = 0

        super(CommentToolDialog, self).__init__()
        self.setWindowTitle("Comment Tool")
        self.resize(800, 800)

        # grid layout
        self.gridLayout = QtWidgets.QGridLayout()

        self.menuBar()

        # textfield
        self.showTextLayout()

        # input text
        self.inputTextLayout()

        # set Layout
        self.setLayout(self.gridLayout)

    def showEvent(self, event):
        """asks the user right at the start if it wants to load a video"""
        self.loadVideofromStartUp()

    def closeEvent(self, event):
        """if the Comment Tool is closed but the Video window is still open it closes the video"""
        self.closeVideo()

    def resizeEvent(self, size):
        """resize the table if the window is resized"""
        self.showTextTable.resizeRowsToContents()
        self.showTextTable.resizeColumnsToContents()

    def menuBar(self):
        """creates the menuBar in the GUI"""
        menu = QtWidgets.QMenuBar()
        menuFile = QtWidgets.QMenu("File")
        menuComments = QtWidgets.QMenu("Comments")
        menuVideo = QtWidgets.QMenu("Video")

        actionExport = QtWidgets.QAction("Save Comments", self)
        actionImport = QtWidgets.QAction("Reload Comments", self)
        actionClear = QtWidgets.QAction("Clear Comments", self)

        actionOpenVideo = QtWidgets.QAction("Open Video", self)

        actionOpenVideo.triggered.connect(self.openVideo)
        actionExport.triggered.connect(self.exportComments)
        actionImport.triggered.connect(self.loadComments)
        actionClear.triggered.connect(self.clearComments)

        menuFile.addAction(actionExport)
        menuComments.addAction(actionImport)
        menuComments.addAction(actionClear)
        menuVideo.addAction(actionOpenVideo)

        menu.addMenu(menuFile)
        menu.addMenu(menuVideo)
        menu.addMenu(menuComments)
        self.gridLayout.addWidget(menu, 0, 0)

    def showTextLayout(self):
        """creates the Layout to show the comments in the GUI"""
        # create a scroll area to ensure a lot of comments can be created
        showTextScrollArea = QtWidgets.QScrollArea()
        # display of the comments is in a table
        self.showTextTable = QtWidgets.QTableWidget()
        self.showTextTable.setColumnCount(4)
        self.showTextTable.setRowCount(self.rowCount)
        # table is 1. Frame, 2. Comments/Text, 3. button to edit the comment, 4. button to delete the comment
        self.showTextTable.setHorizontalHeaderLabels(["Frame", "Comment", "", ""])
        # resize the table
        self.showTextTable.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.showTextTable.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        # disable the function to edit the table
        self.showTextTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        # hide the index of the rows
        self.showTextTable.verticalHeader().setVisible(False)

        showTextScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        showTextScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        showTextScrollArea.setWidgetResizable(True)
        showTextScrollArea.setWidget(self.showTextTable)

        self.gridLayout.addWidget(showTextScrollArea, 1, 0)

    def inputTextLayout(self):
        """layout to write the comments"""
        inputTextGroup = QtWidgets.QGroupBox()
        inputTextLayout = QtWidgets.QVBoxLayout()
        inputFrameLayout = QtWidgets.QHBoxLayout()
        inputTextLayout.addLayout(inputFrameLayout)
        inputTextGroup.setLayout(inputTextLayout)

        inputFrameCheckBox = QtWidgets.QCheckBox()
        frameLabel = QtWidgets.QLabel("Frame")
        self.inputFrame = QtWidgets.QLineEdit()
        # allow the frame input to only accept integers
        self.inputFrame.setValidator(QtGui.QIntValidator(0, 50000))

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
        """displays the input comments to the showText layout"""
        self.scene = CommentTool.getSceneData()
        comments = self.scene["comments"]
        # change the row count to the number of comments
        self.showTextTable.setRowCount(len(comments))

        # iterate over every comment and display it to the table
        for i in range(len(comments)):
            frame = QtWidgets.QTableWidgetItem(f"{comments[i]['frame']}")
            text = QtWidgets.QTableWidgetItem(f"{comments[i]['text']}")
            delete = QtWidgets.QPushButton("delete")
            edit = QtWidgets.QPushButton("edit")

            self.showTextTable.setItem(i, 0, frame)
            self.showTextTable.setItem(i, 1, text)
            self.showTextTable.setCellWidget(i, 2, edit)
            self.showTextTable.setCellWidget(i, 3, delete)

            self.showTextTable.resizeColumnsToContents()
            self.showTextTable.resizeRowsToContents()

            delete.clicked.connect(self.deleteComment)
            edit.clicked.connect(self.editComment)

    def openVideo(self):
        """opens a File Dialog for the user to select a video"""
        fielName = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Video", "./", "*.mov *.mp4"
        )
        videoPath = str(fielName[0])
        if not videoPath == "":
            self.closeVideo()
            self.loadVideo(videoPath)
            self.loadCommentfromVideo(videoPath)

    def loadVideofromStartUp(self):
        """gets called at startup and asks the user if a video should be opened, then proceeds to open a File Dialog"""
        loadVideoBox = QtWidgets.QMessageBox()
        loadVideoBox.setWindowTitle("Open Video")
        loadVideoBox.setText("Do you want to open a Video?")
        buttonYes = QtWidgets.QMessageBox.Yes
        buttonNo = QtWidgets.QMessageBox.No
        loadVideoBox.setStandardButtons(buttonYes | buttonNo)
        loadVideoBox.setDefaultButton(buttonNo)
        boxValue = loadVideoBox.exec_()
        if boxValue == buttonYes:
            self.openVideo()

    def loadCommentfromVideo(self, movPath: str):
        """checks if in the directory where the video was found a .json file was found
            the json file is loaded if the user agrees

        Parameters:
        videoPath(str): path to the .mov file
        """
        file = movPath.rpartition(".")
        self.commentFilePath = str(file[0]) + ".json"
        # check if json file exists
        if pathlib.Path(self.commentFilePath).exists():
            loadCommentsBox = QtWidgets.QMessageBox()
            loadCommentsBox.setWindowTitle("Comments found")
            loadCommentsBox.setText("Comments found")
            loadCommentsBox.setInformativeText("Do you want to load them?")
            buttonYes = QtWidgets.QMessageBox.Yes
            buttonNo = QtWidgets.QMessageBox.No
            loadCommentsBox.setStandardButtons(buttonYes | buttonNo)
            loadCommentsBox.setDefaultButton(buttonYes)
            boxValue = loadCommentsBox.exec_()
            # if user agrees file is loaded
            if boxValue == buttonYes:
                self.loadComments()
            # if user doesn't want to load the comments, the comments get cleared in case there is still some from the previous session
            else:
                self.clearComments()
        # if no json file is found clear the comments, in case there is still some from the previous session
        else:
            self.clearComments()

    def loadVideo(self, movPath: str):
        """opens a vlc window with the video that was found in the path
            opens vlc as a detached window from QProcess to ensure that both work independently

        Parameters:
        movPath(str) : the path to the .mov file
        """
        operationSystem = platform.system()
        process = QtCore.QProcess()
        filePath = pathlib.Path(movPath)
        # start vlc from linux
        if operationSystem == "Linux":
            process.startDetached(f"/usr/bin/vlc {str(movPath)}")
        # start vlc from windows
        if operationSystem == "Windows":
            print("Windows")
            print(filePath)
            pathlib.WindowsPath(filePath)
            process.setProgram("C:\\Program Files\\VideoLAN\\VLC\\vlc.exe")
            process.setArguments([f"{filePath}"])
            process.startDetached()

    def closeVideo(self):
        """ends the running vlc player
        different commands depending on the operating system
        """
        operationSystem = platform.system()
        if operationSystem == "Linux":
            subprocess.run(["pkill", "vlc"])
        if operationSystem == "Windows":
            subprocess.run(["TASKKILL", "/IM", "VLC.EXE"])

    def addComment(self):
        """add a comment to the directory, reads the input of the Text widgets of the GUI"""
        # if no user input for frame == frame 0
        if not self.inputFrame.text():
            self.frame = 0
        else:
            self.frame = int(self.inputFrame.text())

        # if no text is set, an error warning appears and process is aborted
        if not self.inputText.toPlainText():
            error = QtWidgets.QMessageBox()
            error.warning(self, "Warning", "No input text. No comment added")

        # otherwise get the text from the inputText widget
        # and add the comments to the directory
        # delete the input frame and input text and set the frame to the one that was captured earlier
        else:
            self.text = self.inputText.toPlainText()
            CommentTool.addCommentsToScene(self.frame, self.text)
            # clear input
            self.inputText.clear()
            self.inputFrame.clear()

    def deleteComment(self):
        """delete the comment in the row the button was clicked"""
        button = self.sender()
        index = self.showTextTable.indexAt(button.pos())
        # if the index exists delete the comment
        if index.isValid():
            CommentTool.deleteComment(index.row())
            self.showTextTable.removeRow(index.row())

    def editComment(self):
        """edit the comment in the row the button was clicked"""
        button = self.sender()
        index = self.showTextTable.indexAt(button.pos())
        if index.isValid():
            self.inputText.setText((self.scene["comments"][index.row()]["text"]))
            self.inputFrame.setText(str(self.scene["comments"][index.row()]["frame"]))
            CommentTool.deleteComment(index.row())
            self.showTextTable.removeRow(index.row())

    def exportComments(self):
        """export the comments to a json file"""
        CommentTool.exportCommentsFromStandalone(self.commentFilePath)

    def loadComments(self):
        """loads the json file into the scene and displays it in the showText Layout"""
        if not self.commentFilePath == "":
            CommentTool.readJson(self.commentFilePath)
            self.displayText()

    def clearComments(self):
        """clear data of the comments in directory"""
        CommentTool.clearComments()
        self.displayText()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = CommentToolDialog()
    dialog.show()
    sys.exit(app.exec_())
