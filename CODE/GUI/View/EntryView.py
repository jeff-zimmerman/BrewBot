from PyQt5.QtWidgets import *


class entryUI(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('BrewBot Entry Tool')

        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)

        self.centralLayout = QVBoxLayout()
        self._centralWidget.setLayout(self.centralLayout)

        self._createMenu()
        self._createButtons()
        self._createTable()

    def _createMenu(self):
        # Actions
        self.openAction = QAction('&Open', self)
        self.clearAction = QAction('&Clear Display', self)

        # Add actions to menu
        self.fileMenu = self.menuBar().addMenu('&File')

        self.fileMenu.addAction(self.clearAction)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction('&Exit', self.close)

    def _createButtons(self):
        buttonsLayout = QGridLayout()

        # Button text: layout in grid
        self.buttons = {}
        #         {'Button text': (Row, Column, RowStretch, ColumnStretch)}
        buttons = {'Start Recording': (0, 0, 1, 1),
                   'Record Position': (0, 1, 1, 1),
                   'Save': (1, 0, 1, 2)}

        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1], pos[2], pos[3])
            # Add buttonsLayout to the general layout
        self.buttons['Start Recording'].setCheckable(True)
        self.buttons['Record Position'].setEnabled(False)
        self.centralLayout.addLayout(buttonsLayout)

    def _createTable(self):
        self.row_count = 1
        self.tableWidget = QTableWidget(self.row_count, 4)

        tableLayout = QGridLayout()
        tableLayout.addWidget(self.tableWidget, 0, 0)

        header = self.tableWidget.horizontalHeader()
        for col in range(self.tableWidget.columnCount()):
            header.setSectionResizeMode(col, QHeaderView.Stretch)

        self.centralLayout.addLayout(tableLayout)

    def displayText(self):
        """Get display's text."""
        return self.tableWidget.text()