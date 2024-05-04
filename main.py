from PyQt6.QtCore import Qt
import pandas as pd
import pyqtgraph as pg

import sys
import numpy as np

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


global data
data = pd.DataFrame()

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self.header_labels = [x for x in data.columns]

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(),index.column()]

            return str(value)
    def headerData(self, section, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.header_labels[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)
    
    def setHeaderData(self, section, orientation, data, role) :
        if orientation == Qt.Orientation.Horizontal and role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            try:
                self.header_labels[section] = data
                return True
            except:
                return False
        return super().setHeaderData(section, orientation, data, role)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        
        return self._data.shape[1]

# Main Window
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
        self.dropdown = QComboBox()
        self.dropdown.addItem("Top Source IPs")
        self.dropdown.addItem("Top Destination IPs")
        self.dropdown.addItem("Top Source Ports")
        self.dropdown.addItem("Top Destination Ports")
        layout.addWidget(self.dropdown)

        # Results
        self.result = QLabel("Results")
        layout.addWidget(self.result, 1, 0)

        # Update Button
        btn = QPushButton('Update Selection')
        btn.clicked.connect(self.updateSelection)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn,0,1)


        self.tab3.setLayout(layout)

        # ---------------------------------------
        # Top Correlations Tab

        self.tab4 = QWidget(self)

        # ---------------------------------------
        # Top Correlations Tab

        self.tab5 = QWidget(self)

        # ---------------------------------------
        # Missing Data Tab

        self.tab6 = QWidget(self)

        # TAB LIST
        tab.addTab(tab1,"Import Dataset")
        tab.addTab(self.tab2,"View Raw Table")
        tab.addTab(self.tab3,"Top Traffic")
        tab.addTab(self.tab4,"Correlation Matrix")
        tab.addTab(self.tab5,"Correlation Heat Map")
        tab.addTab(self.tab6,"Missing Data")
        # Graphs? https://www.pythonguis.com/tutorials/pyqt6-plotting-pyqtgraph/
        
        main_layout.addWidget(tab, 0, 0, 2, 1)
        
        self.show()

        # Tab 3 - Top Traffic Function
    def updateSelection(self):
        selected_option = self.dropdown.currentText()
        if selected_option == "Top Source IPs":

            top_ip_counts = self.data["id.orig_h"].value_counts().head(10)
            self.result.setText("IP                         Count\n"+str(self.splitip(top_ip_counts)))
        elif selected_option == "Top Destination IPs":
            top_ip_counts = self.data["id.resp_h"].value_counts().head(10)
            self.result.setText("IP                         Count\n"+str(self.splitip(top_ip_counts)))
        elif selected_option == "Top Source Ports":
            top_ip_counts = self.data["id.orig_p"].value_counts().head(10)
            self.result.setText("Port    Count\n"+str(self.splitip(top_ip_counts)))
        elif selected_option == "Top Destination Ports":
            top_ip_counts = self.data["id.resp_p"].value_counts().head(10)
            self.result.setText("Port    Count\n"+str(self.splitip(top_ip_counts)))
            
    def splitip(self, ip):
        list = ip.to_string().split("\n")[1:]
        total = ""
        for i, j in enumerate(list):
            total += str(j) + "\n"
        return total

        # Data import function
    def ImportData(self):
        if self.label.text() != "No File Selected":
            try:
                self.data = pd.read_csv(self.path, sep='|')
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

        # Close Window
    def Close(self):
        sys.exit(self)
    
        # File Explorer
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

        # Build out Tabs
    def buildTabContents(self):
        self.createTable(self.tab2, self.data)
        corrTable = self.genCorr()
        labeledCorrTable = corrTable.copy()
        labeledCorrTable.insert(loc=0, column="", value=labeledCorrTable.columns)
        self.createTable(self.tab4, labeledCorrTable)
        self.createTab5(corrTable)
        missData = self.missingData()
        self.createTable(self.tab6, missData)

    def getTopIPs(self):
        
        IPCounts = self.data.value_counts(sort=True, dropna=True)

        return IPCounts

    def createTable(self, tab, data):
        layout = QVBoxLayout()
        table = QTableView()
        model = TableModel(data)
        table.setModel(model)

        layout.addWidget(table)
        tab.setLayout(layout)

    def genCorr(self):
        corrTable = self.data.corr(numeric_only=True)
        return corrTable
    
    def missingData(self):
        total = self.data.isnull().sum().sort_values(ascending=False)
        percent = (self.data.isnull().sum()/self.data.isnull().count()).sort_values(ascending=False)
        missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
        missing_data.insert(loc=0, column="featureName", value=self.data.columns)
        return missing_data.head(20)

    def createTab5(self, corrMap):
        layout = QVBoxLayout()

        x = "                                " + corrMap.columns
        xdict = dict(enumerate(x))

        xaxis = pg.AxisItem(orientation='bottom')
        xaxis.setTicks([xdict.items()])

        yaxis = pg.AxisItem(orientation='left')
        yaxis.setTicks([xdict.items()])

        plot = pg.PlotItem(axisItems={'bottom': xaxis, 'left': yaxis})

        graphWidget = pg.ImageView(view=plot)
        graphWidget.setImage(corrMap.to_numpy())
        colors = [(0,0,0),(29, 14, 54),(65, 31, 120),(247, 79, 79),(252, 134, 134),(255, 186, 158),(255, 
        255, 255)]
        cmap = pg.ColorMap(pos=np.linspace(0.0, 1.0, 7), color=colors)
        graphWidget.setColorMap(cmap)

        layout.addWidget(graphWidget)
        self.tab5.setLayout(layout)

app = QApplication(sys.argv)
MainMenu = MainMenu()
MainMenu.show()
sys.exit(app.exec())
