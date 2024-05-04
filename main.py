import pandas as pd
import pyqtgraph as pg

import sys
import os

import matplotlib.pyplot as plt
import seaborn as sns

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


global data
data = pd.DataFrame()

    # idk how tables work
class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self.hheaders = [x for x in data.columns]

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(),index.column()]

            return str(value)
    #def headerData(self, section, orientation, role):
    #    if orientation == Qt.Orientation.Horizontal:
    #        return self.header_labels[section]
    #    return QAbstractTableModel.headerData(self, section, orientation, role)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        
        return self._data.shape[1]


class MainMenu(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Visualizer 1.0")
        self.setMinimumSize(QSize(700,500))

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

        self.tab2 = QWidget(self)

        # ---------------------------------------
        # Top IPs Tab

        self.tab3 = QWidget(self)
        layout = QGridLayout()

        # Drop Down Menu
        dropdown = QComboBox()
        dropdown.addItem("Top Source IPs")
        dropdown.addItem("Top Destination IPs")
        dropdown.addItem("Top Source Ports")
        dropdown.addItem("Top Destination Ports")
        layout.addWidget(dropdown)

        label = QLabel("Top 10:")
        datalabel = QLabel("Data")

        layout.addWidget(label, 1, 0)
        layout.addWidget(datalabel, 1, 1)


        self.tab3.setLayout(layout)

        # ---------------------------------------
        # Top Correlations Tab

        self.tab4 = QWidget(self)

        # ---------------------------------------
        # Missing Data Tab

        self.tab5 = QWidget(self)

        # TAB LIST
        tab.addTab(tab1,"Import Dataset")
        tab.addTab(self.tab2,"View Raw Table")
        tab.addTab(self.tab3,"Top Traffic")
        tab.addTab(self.tab4,"Top Correlations")
        tab.addTab(self.tab5,"Missing Data")
        # Graphs? https://www.pythonguis.com/tutorials/pyqt6-plotting-pyqtgraph/
        
        main_layout.addWidget(tab, 0, 0, 2, 1)
        
        self.show()

    
    def ImportData(self):
        if self.label.text() != "No File Selected":
            try:
                self.data = pd.read_csv(self.path, sep='|')
                print(self.data.head())
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Success!")
                dlg.setText("File Successfully Imported.")
                dlg.exec()
                self.buildTabContents()
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

    def buildTabContents(self):
        self.createTable(self.tab2, self.data)
        print("Finding Top IPS")
        srcIPCounts, srcPortCounts, destIPCounts, destPortCounts = self.getTrafficFreq()
        print("Creating Tab3")
        self.createTable(self.tab3, srcIPCounts)
        print("Generating Correlations")
        corrTable = self.genCorr()
        print("Creating Tab4")
        self.createTable(self.tab4, corrTable)
        print("Identifying Missing Data")
        missData = self.missingData()
        print("Creating Tab5")
        self.createTable(self.tab5, missData)

    def getTrafficFreq(self):
        
        srcIPCounts = self.data["id.orig_h"].value_counts().to_frame()

        srcPortCounts = self.data["id.orig_p"].value_counts().to_frame()

        destIPCounts = self.data["id.resp_h"].value_counts().to_frame()

        destPortCounts = self.data["id.resp_p"].value_counts().to_frame()

        return srcIPCounts, srcPortCounts, destIPCounts, destPortCounts

    def createTable(self, tab, data):
        layout = QVBoxLayout()
        table = QTableView()
        model = TableModel(data)
        table.setModel(model)

        layout.addWidget(table)
        tab.setLayout(layout)

    def genCorr(self):
        corrTable = self.data.corr(numeric_only=True)
        print(corrTable)
        return corrTable
    
    def missingData(self):
        total = self.data.isnull().sum().sort_values(ascending=False)
        percent = (self.data.isnull().sum()/self.data.isnull().count()).sort_values(ascending=False)
        missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
        missing_data.insert(loc=0, column="featureName", value=self.data.columns)
        return missing_data.head(20)

app = QApplication(sys.argv)
MainMenu = MainMenu()
MainMenu.show()
sys.exit(app.exec())
