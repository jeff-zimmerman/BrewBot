import sys
from PyQt5.QtWidgets import QApplication
from Controller.EntryCtrl import entryCtrl
from View.EntryView import entryUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = entryUI()
    view.show()
    control = entryCtrl(view)
    sys.exit(app.exec_())