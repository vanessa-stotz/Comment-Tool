#!/usr/bin/env python

import sys

from PySide2 import QtWidgets, QtCore

from CommentTool import writeJson, readJson




class CommentToolDialog(QtWidgets.QDialog):
    
    def __init__(self, parent = None) :

        #variables
        self.frame = 0
        self.text = ""
        self.scene = {}

        self.scene["sceneName"] = ""
        self.scene["comments"] = []

        comments = {}


        super(CommentToolDialog, self).__init__()
        self.setWindowTitle("Comment Tool")
        self.resize(800,400)

        #grid layout
        self.gridLayout = QtWidgets.QGridLayout()

        # textfield
        self.showTextLayout()

        #input text
        self.inputTextLayout()

        #set Layout
        self.setLayout(self.gridLayout)


        #readJson()
        #writeJson()


    def showTextLayout(self):
        showTextGroup = QtWidgets.QGroupBox("Display Text")
        self.gridLayout.addWidget(showTextGroup, 0, 0)
        showTextLayout = QtWidgets.QVBoxLayout()
        showTextGroup.setLayout(showTextLayout)

        showText = QtWidgets.QTextEdit()
        showText.isReadOnly()
        showText.setDisabled(True)
        showTextLayout.addWidget(showText)




    def inputTextLayout(self):
        inputTextGroup = QtWidgets.QGroupBox("Input Text")
        self.gridLayout.addWidget(inputTextGroup, 1, 0)
        inputTextLayout = QtWidgets.QVBoxLayout()

        
        inputFrameLayout = QtWidgets.QHBoxLayout()
        inputTextLayout.addLayout(inputFrameLayout)
        inputTextGroup.setLayout(inputTextLayout)

        inputFrameCheckBox = QtWidgets.QCheckBox()
        frameLabel = QtWidgets.QLabel("Frame")
        self.inputFrame = QtWidgets.QLineEdit()
        #self.inputFrame.setValidator(QtCore.QObject.QIntValidator())
        
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



    def displayText(self):
        ...


    def addComment(self):
        print("new Comment")
        self.frame = int(self.inputFrame.text())
        print(self.frame)


        



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = CommentToolDialog()
    dialog.show()
    sys.exit(app.exec_())