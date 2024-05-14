import sys
from PySide2 import QtWidgets
import main

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = main.CommentToolDialog()
    dialog.show()
    sys.exit(app.exec_())