import sys, csv
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from time import sleep, time
from pathlib import Path

from CODE.GUI.record.arduinoControl import *


class EntryUI(QMainWindow):

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
        #Actions
        self.openAction = QAction('&Open', self)

        #Add actions to menu
        self.fileMenu = self.menuBar().addMenu('&File')
        self.fileMenu.addAction('&Exit', self.close)
        self.fileMenu.addAction(self.openAction)

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
        self.centralLayout.addLayout(tableLayout)

    def displayText(self):
        """Get display's text."""
        return self.tableWidget.text()

    def clearDisplay(self):
        """Clear the display."""
        self.row_count = 0
        self.tableWidget.setRowCount(self.row_count)


class entryCtrl(QObject):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        self._view = parent
        self.basepath = str(Path(__file__).parents[3])
        self.tableWidget = self._view.tableWidget
        self.buttons = self._view.buttons
        self._connectSignals()

        self.connectArduino()

    def _connectSignals(self):
        self.buttons['Start Recording'].clicked.connect(self._recordStart)
        self.buttons['Record Position'].clicked.connect(self._recordPos)
        self.buttons['Save'].clicked.connect(self._saveTable)
        self._view.openAction.triggered.connect(self._openTable)


    def connectArduino(self) -> object:

        self.connectThread = QThread()
        self.connectWorker = connectArduino()

        self.connectWorker.moveToThread(self.connectThread)

        self.connectThread.started.connect(self.connectWorker.initArduino)
        self.connectWorker.connect_status.connect(print)
        self.connectWorker.update_pos.connect(self._displayPos)

        self.connectThread.start()

    def _recordStart(self):
        if self.buttons['Start Recording'].isChecked():
            self.buttons['Start Recording'].setText('Stop Recording')
            self.buttons['Record Position'].setEnabled(True)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, QTableWidgetItem(str(0)))

            self.connectWorker.recordBtnState = True
            self.connectWorker.time_start = time.time()

            self.tableWidget.insertRow(self.tableWidget.rowCount())
        else:
            self.buttons['Start Recording'].setText('Start Recording')
            self.buttons['Record Position'].setEnabled(False)

            self.connectWorker.recordBtnState = False

            self.tableWidget.insertRow(self.tableWidget.rowCount())


    def _recordPos(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.connectWorker.time_start = time.time()

    def _displayPos(self, values):
        '''display real time values of recordThread signals'''
        for cell, val in enumerate(values):
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, cell, QTableWidgetItem(str(val)))

    def _saveTable(self):
        if not hasattr(self, 'filename'):
            self.filename = QInputDialog.getText(self._view,
                                            'Save Routine',
                                            'Routine Name:'
                                            )[0]
        # opens file to record positions and times in
        with open(f'{self.basepath}/RECORD/{self.filename}.csv', mode='w+') as f:
            writer = csv.writer(f)
            for row in range(self.tableWidget.rowCount()):
                rowdata = []
                for column in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(row, column)
                    if item is not None:
                        rowdata.append(item.text())
                    else:
                        rowdata.append('')
                writer.writerow(rowdata)
            f.close()

    def _openTable(self):

        path = QFileDialog.getOpenFileName(parent=self._view,
                                           caption='Open File',
                                           directory=self.basepath,
                                           filter='CSV(*.csv)')[0]

        if path:
            with open(path, 'rt') as stream:
                self.tableWidget.setRowCount(0)
                self.tableWidget.setColumnCount(0)
                for rowdata in csv.reader(stream):
                    row = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row)
                    self.tableWidget.setColumnCount(len(rowdata))
                    for column, data in enumerate(rowdata):
                        item = QTableWidgetItem(data)
                        self.tableWidget.setItem(row, column, item)

            self.filename = Path(path).stem


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = EntryUI()
    view.show()
    control = entryCtrl(view)
    # connect = connectArduino()
    # connect.initArduino()
    sys.exit(app.exec_())
