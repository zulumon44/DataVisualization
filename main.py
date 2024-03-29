import pandas as pd
import pyqtgraph as pg

import sys
import os

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


global data
data = pd.DataFrame()

    # idk how tables work
class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
    
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]


class MainMenu(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Visualizer 1.0")
        self.setMinimumSize(QSize(300,200))

        # Layout of Tabs
        main_layout = QGridLayout(self)
        self.setLayout(main_layout)

        tab = QTabWidget(self)


        # ---------------------------------------
        # Data Import Tab
        
        tab1 = QWidget(self)
        tab1.setStyleSheet("*{font-size: 12pt;}")
        layout = QGridLayout()

        # File Selector Button
        btn = QPushButton('Select File')
        btn.clicked.connect(self.getFileName)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn,0,1)

        # Review File Selector 
        self.label = QLabel("No File Selected")
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label,1,0,1,3)

        # Analyze Button
        go = QPushButton('Import')
        go.clicked.connect(self.ImportData)
        layout.addWidget(go,2,0)
        
        # Close Button
        close = QPushButton('Close')
        close.clicked.connect(self.Close)
        layout.addWidget(close,2,2)

        tab1.setLayout(layout)


        # ---------------------------------------
        # Data View Tab

        tab2 = QWidget(self)
        layout = QGridLayout()

        btn = QPushButton('Refresh File')
        btn.clicked.connect(self.ImportData)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # layout.addWidget(btn,0,0)
        # Idk if refresh button is necessary

        self.table = QTableView()
        self.model = TableModel(data)
        self.table.setModel(self.model)

        layout.addWidget(self.table)
        tab2.setLayout(layout)

        # ---------------------------------------
        # Top IPs Tab

        tab3 = QWidget(self)
        layout = QGridLayout()


        tab3.setLayout(layout)

        # TAB LIST
        tab.addTab(tab1,"Import Dataset")
        tab.addTab(tab2,"View Raw Table")
        tab.addTab(tab3,"Top IP\'s")
        # Graphs? https://www.pythonguis.com/tutorials/pyqt6-plotting-pyqtgraph/
        
        main_layout.addWidget(tab, 0, 0, 2, 1)

        
        self.show()

    
    def ImportData(self):
        if self.label.text() != "No File Selected":
            try:
                data = pd.read_csv(self.path)
                print(data.head())
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Success!")
                dlg.setText("File Successfully Imported.")
                dlg.exec()
            except Exception as e:
                print(e)
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("ERROR!")
            dlg.setText("You Must Select a File")
            dlg.exec()
        print("Done")

    def Close(self):
        sys.exit(self)
    
    def getFileName(self):
        file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a Dataset',
            directory=".",
            filter=file_filter,
            initialFilter='Data File (*.xlsx *.csv *.dat)'
        )
        self.label.setText(str(response[0]).rsplit('/', 1)[-1])
        self.path = str(response[0])



app = QApplication(sys.argv)
MainMenu = MainMenu()
MainMenu.show()
sys.exit(app.exec())
