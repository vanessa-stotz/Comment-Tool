#!/usr/bin/env python

import sys

from PySide2 import QtWidgets

from CommentTool import writeJson, readJson




class CommentToolDialog(QtWidgets.QDialog):
    
    def __init__(self, parent = None) :
        super(CommentToolDialog, self).__init__()
        self.setWindowTitle("Comment Tool")
        self.resize(800,400)

        # self.gridLayout = QtWidgets.QGridLayout()

        # # textfield
        # displayTextGroupBox = QtWidgets.QGroupBox("Display Text")
        # self.gridLayout.addWidget(displayTextGroupBox,0,0)

        # #input text
        # self.inputTextDisplay()
        readJson()
        #writeJson()



    def inputTextDisplay(self):

        inputTextDisplay = QtWidgets.QGroupBox("Input Text")



        



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = CommentToolDialog()
    dialog.show()
    sys.exit(app.exec_())