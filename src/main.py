#!/usr/bin/env python

import sys

from PySide2 import QtWidgets, QtGui

from CommentTool import writeJson, readJson, addCommentsToScene, getSceneDict




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

        length = len(self.scene["comments"])
        print(f"length  start {length}")

        #readJson()
        #writeJson()


    def showTextLayout(self):
        showTextGroup = QtWidgets.QGroupBox("Display Text")
        self.gridLayout.addWidget(showTextGroup, 0, 0)
        showTextLayout = QtWidgets.QVBoxLayout()
        showTextGroup.setLayout(showTextLayout)

        self.showText = QtWidgets.QTextEdit()
        self.showText.isReadOnly()
        self.showText.setDisabled(True)
        showTextLayout.addWidget(self.showText)




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



    # def displayText(self):
    #     self.scene = getSceneDict()
    #     for i in self.scene["comments"] :
    #         frame = f"{['frame']}"
    #         text = f"{['text']}"
    #         self.showText.setText(f"Frame {frame}\n")
    #         self.showText.setText(f"{text}\n")
    #         self.showText.setText("____________________")
        


    def addComment(self):

        print("new Comment")
        
        #if no user input for frame == frame 0
        if not self.inputFrame.text() :
            self.frame = 0
        else :
            self.frame = int(self.inputFrame.text())


        self.text = self.inputText.toPlainText()
        print(self.frame)
        print(self.text)

        addCommentsToScene(self.frame, self.text)

        
        #clear input 
        self.inputText.clear()
        self.inputFrame.clear()






if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = CommentToolDialog()
    dialog.show()
    sys.exit(app.exec_())