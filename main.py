#import os
import pandas as pd


# csvFile = pd.read_csv('CTU-IoT-Malware-Capture-1-1conn.log.labeled.csv')
# print(csvFile.head())
import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

#(QApplication, QWidget, QPushButton, QTextEdit, QComboBox, QFileDialog,QHBoxLayout, QVBoxLayout)
    
class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Visualizer 1.0")
        self.setMinimumSize(QSize(300,125))
        # Layout of Tabs
        main_layout = QGridLayout(self)
        self.setLayout(main_layout)

        tab = QTabWidget(self)

        tab1 = QWidget(self)
        layout = QGridLayout()
        # File Selector Button
        btn = QPushButton('Select File')
        btn.clicked.connect(self.getFileName)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn,0,1)

        # Review File Selector 
        self.textbox = QLineEdit()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.textbox,1,0,1,3)

        # Analyze Button
        go = QPushButton('Import')
        go.clicked.connect(self.ImportData)
        layout.addWidget(go,2,0)
        
        # Close Button
        close = QPushButton('Close')
        close.clicked.connect(self.Close)
        layout.addWidget(close,2,2)

        tab1.setLayout(layout)


        
        tab.addTab(tab1,"Import Dataset")
        
        main_layout.addWidget(tab, 0, 0, 2, 1)
        # main_layout.addWidget(QPushButton('Save'), 2, 0,
        #                       alignment=Qt.AlignmentFlag.AlignLeft)
        # main_layout.addWidget(QPushButton('Cancel'), 2, 0,
        #                       alignment=Qt.AlignmentFlag.AlignRight)
        
        self.show()

    def ImportData(self):
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
        self.textbox.setText(str(response[0]))





app = QApplication(sys.argv)
MainMenu = MainMenu()
MainMenu.show()
sys.exit(app.exec())
