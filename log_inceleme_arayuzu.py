# read csv file
from PyQt6 import QtGui
from PyQt6.QtWidgets import QFileDialog, QAbstractItemView, QHeaderView, QWidget, QApplication, QMessageBox, QLineEdit, QPushButton, QVBoxLayout, QScrollArea, QCheckBox, QTableWidget, QTableWidgetItem, QMenuBar, QInputDialog, QLabel
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import yaml
from PyQt6.QtCore import Qt, pyqtSignal

# python -m venv myenv
# pip ile gerekli kutuphanleri yukle
# myenv\Scripts\activate
# cd C:\Users\aycivan\Desktop\Repositories\es_test_applications\CSV_Reader
# python setup.py build_exe

# pip install PyQt6 matplotlib numpy pyyaml


def read_from_csv(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    return lines


class MouseClickButton(QPushButton):

    clicked = pyqtSignal(str)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            # Emit the signal with the title as parameter
            self.clicked.emit("right")
        elif event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit("left")

        super().mousePressEvent(event)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.slipLineCharacter = ';'

        self.mathCalculationWidget = QWidget()
        self.filterWidget = QWidget()
        self.reviewNoteWidget = QWidget()
        self.conditionalAnalysisWidget = QWidget()
        self.programmerAnalysisWidget = QWidget()
    

        # read file path from yaml file
        if os.path.exists('CSV_reader_Config/file_path.yaml'):
            with open('CSV_reader_Config/file_path.yaml', 'r') as f:
                self.pathCSV = yaml.load(f, Loader=yaml.FullLoader)
        
        self.selectedPath = ''
                
        self.version = "5.5.0"
        self.CppArrayData = ""

        self.setWindowTitle('CSV Reader V' + self.version)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setGeometry(300, 50, 400, 400)

        menuStyle = """QMenu {background-color: #E1E1E1;
                            color: black;
                            border-style: solid;
                            border-width: 1px;
                            border-color: #1E1E1E;
                            border-radius: 10px;
                            font: bold 14px;
                            padding: 3px;
                            margin: 2px;}
                            QMenu::item:selected {background-color: #1E1E1E;
                            color: #6ECC78;
                            border-color: #777;}"""
        buttonStyle = """QPushButton {
                            background-color: #E1E1E1;
                            color: black;
                            border-style: solid;
                            border-width: 1px;
                            border-color: #1E1E1E;
                            border-radius: 10px;
                            font: bold 14px;
                            padding: 3px;
                            margin: 2px;
                        }
                        QPushButton:hover {
                            background-color: #1E1E1E;
                            color: #6ECC78;
                            border-color: #777;
                        QPushButton:pressed {
                            background-color: #6ECC78;
                            color: black;
                            border-color: #1E1E1E;
                        }}
                        """
        
        # add qmenu
        self.menuBar = QMenuBar()
        self.menuBar.setNativeMenuBar(False)
        self.fileMenu = self.menuBar.addMenu('File')
        self.fileMenu.setStyleSheet(menuStyle)
        self.fileMenu.addAction('Open CSV File', self.read_csv)
        self.fileMenu.addAction('Exit', self.close)

        self.mathMenu = self.menuBar.addMenu('Math')
        self.mathMenu.setStyleSheet(menuStyle)
        self.mathMenu.addAction('Math Calculation', self.mathCalculationWidget.show)
        self.mathMenu.addAction('Filters', self.filterWidget.show)
        self.mathMenu.addAction('Conditional Analysis', self.conditionalAnalysisWidget.show)
        self.mathMenu.addAction('Programmer Analysis', self.programmerAnalysisWidget.show)

        self.configMenu = self.menuBar.addMenu('Config')
        self.configMenu.setStyleSheet(menuStyle)
        self.configMenu.addAction('Set Separator', self.setSeparator)
        self.configMenu.addAction('Review Note', self.reviewNoteWidget.show)

        self.helpMenu = self.menuBar.addMenu('Help')
        self.helpMenu.setStyleSheet(menuStyle)
        self.helpMenu.addAction('About', self.about)
        self.helpMenu.addAction('Help', self.help)
        self.helpMenu.addAction('Thanks', self.thanks)

        self.button = QPushButton('Open CSV file')
        self.button.clicked.connect(self.read_csv)
        self.button.setStyleSheet(buttonStyle)

        self.checkboxStyle = """
                QCheckBox {
                    background-color: #E1E1E1;
                    color: black;
                    border: none;
                    font: bold 14px;
                    padding: 3px;
                    margin: 2px;
                }
                QCheckBox:hover {
                    background-color: #1E1E1E;
                    color: #6ECC78;
                    border-color: #777;
                }
                QCheckBox::indicator {
                    width: 13px;
                    height: 13px;
                }
            """
        
        self.lineEditStyle = """
                QLineEdit {
                    background-color: #E6E6E6;
                    color: #808080;
                    border-style: solid;
                    border-width: 1px;
                    border-color: #1E1E1E;
                    border-radius: 5px;
                    font: bold 14px;
                    padding: 3px;
                    margin: 2px;
                }
                QLineEdit:hover {
                    background-color: #FAFAFA;
                    color: black;
                }
                QLineEdit:focus {
                    background-color: #FAFAFA;
                    color: black;
                    border: 2px solid #777;
                }
            """
        # add draw on the same graph checkbox
        self.drawOnTheSameGraphCheckBox = QCheckBox('Draw On the Same Graph')
        self.drawOnTheSameGraphCheckBox.setChecked(False)
        self.drawOnTheSameGraphCheckBox.setStyleSheet(self.checkboxStyle)

        # add y axis twinx checkbox
        self.yAxisTwinxCheckBox = QCheckBox('Y Axis Twinx')
        self.yAxisTwinxCheckBox.setChecked(False)
        self.yAxisTwinxCheckBox.setStyleSheet(self.checkboxStyle)

        # add separate line
        self.line2 = QWidget()
        self.line2.setFixedHeight(1)
        self.line2.setStyleSheet('background-color: black')

        self.fftCheckBox = QCheckBox('FFT on')
        self.fftCheckBox.setChecked(False)
        self.fftCheckBox.stateChanged.connect(self.fftCheckBoxChanged)
        self.fftCheckBox.setStyleSheet(self.checkboxStyle)

        # add separate line
        self.line3 = QWidget()
        self.line3.setFixedHeight(1)
        self.line3.setStyleSheet('background-color: black')

        self.fftFrequency = QLineEdit()
        self.fftFrequency.setPlaceholderText('Sample Frequency')
        self.fftFrequency.setDisabled(True)
        self.fftFrequency.setStyleSheet(self.lineEditStyle)

        self.openRawData = QCheckBox('Open Raw Data In Table')
        self.openRawData.setChecked(False)
        self.openRawData.setStyleSheet(self.checkboxStyle)

        # add separator line
        self.line = QWidget()
        self.line.setFixedHeight(1)
        self.line.setStyleSheet("""
                    background-color: black;
                    color: black;
                    border: none;
                    padding: 3px;
                    margin: 2px;
                    """)

        # add mean on the same graph checkbox
        self.meanCheckBox = QCheckBox('Mean On')
        self.meanCheckBox.setChecked(False)
        self.meanCheckBox.setStyleSheet(self.checkboxStyle)

        self.searchField = QLineEdit()
        self.searchField.setPlaceholderText('Search')
        self.searchField.returnPressed.connect(self.search)
        self.searchField.textChanged.connect(self.search)
        self.searchField.setDisabled(True)
        self.searchField.setStyleSheet(self.lineEditStyle)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.drawOnTheSameGraphCheckBox)
        self.layout.addWidget(self.yAxisTwinxCheckBox)
        self.layout.addWidget(self.line2)
        self.layout.addWidget(self.fftCheckBox)
        self.layout.addWidget(self.fftFrequency)
        self.layout.addWidget(self.openRawData)
        self.layout.addWidget(self.line)
        self.layout.addWidget(self.meanCheckBox)
        self.layout.addWidget(self.line3)
        self.layout.addWidget(self.searchField)
        self.layout.setMenuBar(self.menuBar)
  
        self.spacer = QWidget()
        self.layout.addWidget(self.spacer)

        self.setLayout(self.layout)

        self.aHolder = 0
        self.bHolder = 0
        self.lineCounter = 0
        self.titleList = []
        self.colors = ['red', 'green', 'purple',
                       'orange', 'cyan', 'magenta', 'yellow', 'brown', 'grey', 'olive', 'lime', 'teal', 'navy', 'black']
        self.pathCSV = ''
        self.ax_title = ''
        self.counter_for_flight_mode = 0

        self.data_selected_one = []
        self.data_selected_two = []
        self.dataOneOn = False
        self.dataTwoOn = False
        self.qButton = QPushButton()

        self.rawDataWidget = QWidget()

        # add math calculation widget
        self.mathCalculationWidget.setWindowTitle("Calculation")
        self.mathCalculationWidget.resize(250, 150)
        self.mathCalculationWidget.move(10, 30)
        self.mathCalculationWidget.show()

        self.filterWidget.setWindowTitle("Filter")
        self.filterWidget.resize(250, 100)
        self.filterWidget.move(10, 460)
        self.filterWidget.show()

        # add log review note
        self.reviewNoteWidget.setWindowTitle("Note Review")
        self.reviewNoteWidget.resize(250, 300)
        self.reviewNoteWidget.move(10, 600)
        self.reviewNoteWidget.show()
        
        # add conditional analysis
        self.conditionalAnalysisWidget.setWindowTitle("Conditional Analysis")
        self.conditionalAnalysisWidget.resize(250, 300)
        self.conditionalAnalysisWidget.move(610, 30)
        self.conditionalAnalysisWidget.show()
        
        # add programmer analysis
        self.programmerAnalysisWidget.setWindowTitle("Programmer Analysis")
        self.programmerAnalysisWidget.resize(250, 100)
        self.programmerAnalysisWidget.move(610, 375)
        self.programmerAnalysisWidget.show()
        
        # add textbox for get number for math calculation
        self.mathCalculationTextBox = QLineEdit()
        self.mathCalculationTextBox.setPlaceholderText('Enter Number')
        self.mathCalculationTextBox.setStyleSheet(self.lineEditStyle)
        self.mathCalculationTextBox.setValidator(QtGui.QDoubleValidator().setNotation(QtGui.QDoubleValidator.Notation.StandardNotation))

        self.plusCheckBox = QCheckBox('+')
        self.plusCheckBox.setChecked(False)
        self.plusCheckBox.setStyleSheet(self.checkboxStyle)
        self.minusCheckBox = QCheckBox('-')
        self.minusCheckBox.setChecked(False)
        self.minusCheckBox.setStyleSheet(self.checkboxStyle)
        self.multiplyCheckBox = QCheckBox('*')
        self.multiplyCheckBox.setChecked(False)
        self.multiplyCheckBox.setStyleSheet(self.checkboxStyle)
        self.divideCheckBox = QCheckBox('/')
        self.divideCheckBox.setChecked(False)
        self.divideCheckBox.setStyleSheet(self.checkboxStyle)

        # add separator line
        self.line4 = QWidget()
        self.line4.setFixedHeight(1)
        self.line4.setStyleSheet("""
                    background-color: black;
                    color: black;
                    border: none;
                    padding: 3px;
                    margin: 2px;
                    """)

        # add line edit for start and end point
        self.startPoint = QLineEdit()
        self.startPoint.setPlaceholderText('Start Point')
        self.startPoint.setStyleSheet(self.lineEditStyle)
        self.startPoint.setValidator(QtGui.QIntValidator())
        self.endPoint = QLineEdit()
        self.endPoint.setPlaceholderText('End Point')
        self.endPoint.setStyleSheet(self.lineEditStyle)
        self.endPoint.setValidator(QtGui.QIntValidator())

        # add checkbox for use start and end point
        self.startEndPointCheckBox = QCheckBox('Use Start and End Point')
        self.startEndPointCheckBox.setChecked(False)
        self.startEndPointCheckBox.setStyleSheet(self.checkboxStyle)

        # add separator line
        self.line5 = QWidget()
        self.line5.setFixedHeight(1)
        self.line5.setStyleSheet("""
                    background-color: black;
                    color: black;
                    border: none;
                    padding: 3px;
                    margin: 2px;
                    """)
        
        # multiple line new label
        self.multipleLineLabel = QLineEdit()
        self.multipleLineLabel.setPlaceholderText('Enter Multiple Line Label')
        self.multipleLineLabel.setStyleSheet(self.lineEditStyle)
        

        # add multiple two line checkbox
        self.multipleTwoLineCheckBox = QCheckBox('Multiple Two Line')
        self.multipleTwoLineCheckBox.setChecked(False)
        self.multipleTwoLineCheckBox.setStyleSheet(self.checkboxStyle)

        self.mathCalculationLayout = QVBoxLayout()
        self.mathCalculationLayout.addWidget(self.mathCalculationTextBox)
        self.mathCalculationLayout.addWidget(self.plusCheckBox)
        self.mathCalculationLayout.addWidget(self.minusCheckBox)
        self.mathCalculationLayout.addWidget(self.multiplyCheckBox)
        self.mathCalculationLayout.addWidget(self.divideCheckBox)
        self.mathCalculationLayout.addWidget(self.line4)
        self.mathCalculationLayout.addWidget(self.startPoint)
        self.mathCalculationLayout.addWidget(self.endPoint)
        self.mathCalculationLayout.addWidget(self.startEndPointCheckBox)
        self.mathCalculationLayout.addWidget(self.line5)
        self.mathCalculationLayout.addWidget(self.multipleLineLabel)
        self.mathCalculationLayout.addWidget(self.multipleTwoLineCheckBox)   
        self.mathCalculationWidget.setLayout(self.mathCalculationLayout)
        self.mathCalculationWidget.setWindowIcon(QtGui.QIcon('icon.ico'))

        self.movingAverageCheckBox = QCheckBox('Moving Average')
        self.movingAverageCheckBox.setChecked(False)
        self.movingAverageCheckBox.setStyleSheet(self.checkboxStyle)

        self.movingAveragePeriod = QLineEdit()
        self.movingAveragePeriod.setPlaceholderText('Period')
        self.movingAveragePeriod.setStyleSheet(self.lineEditStyle)
        self.movingAveragePeriod.setValidator(QtGui.QIntValidator())
        

        self.filterLayout = QVBoxLayout()
        self.filterLayout.addWidget(self.movingAveragePeriod)
        self.filterLayout.addWidget(self.movingAverageCheckBox)
        self.filterWidget.setLayout(self.filterLayout)
        self.filterWidget.setWindowIcon(QtGui.QIcon('icon.ico'))


        self.reviewNoteSaveButton = QPushButton('Save')
        self.reviewNoteSaveButton.setStyleSheet(buttonStyle)
        self.reviewNoteSaveButton.clicked.connect(self.review_note_save)
        
        self.reviewNoteRichtextBox = QTableWidget()
        self.reviewNoteRichtextBox.setColumnCount(1)
        self.reviewNoteRichtextBox.setHorizontalHeaderLabels(["Review Notes"])
        self.reviewNoteRichtextBox.setRowCount(100)
        self.reviewNoteRichtextBox.setItem(0, 0, QTableWidgetItem(''))
        self.reviewNoteRichtextBox.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.reviewNoteRichtextBox.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.reviewNoteLayout = QVBoxLayout()
        self.reviewNoteLayout.addWidget(self.reviewNoteSaveButton)
        self.reviewNoteLayout.addWidget(self.reviewNoteRichtextBox)
        self.reviewNoteWidget.setLayout(self.reviewNoteLayout)
        self.reviewNoteWidget.setWindowIcon(QtGui.QIcon('icon.ico'))
        
        # add  "<", ">", "<=", ">=", "=" checkbox for conditional analysis
        self.lessThanCheckBox = QCheckBox('<')
        self.lessThanCheckBox.setChecked(False)
        self.lessThanCheckBox.setStyleSheet(self.checkboxStyle)
        self.lessThanCheckBox.stateChanged.connect(self.uncheckOthers)

        self.greaterThanCheckBox = QCheckBox('>')
        self.greaterThanCheckBox.setChecked(False)
        self.greaterThanCheckBox.setStyleSheet(self.checkboxStyle)
        self.greaterThanCheckBox.stateChanged.connect(self.uncheckOthers)

        self.lessThanEqualCheckBox = QCheckBox('<=')
        self.lessThanEqualCheckBox.setChecked(False)
        self.lessThanEqualCheckBox.setStyleSheet(self.checkboxStyle)
        self.lessThanEqualCheckBox.stateChanged.connect(self.uncheckOthers)

        self.greaterThanEqualCheckBox = QCheckBox('>=')
        self.greaterThanEqualCheckBox.setChecked(False)
        self.greaterThanEqualCheckBox.setStyleSheet(self.checkboxStyle)
        self.greaterThanEqualCheckBox.stateChanged.connect(self.uncheckOthers)

        self.equalCheckBox = QCheckBox('=')
        self.equalCheckBox.setChecked(False)
        self.equalCheckBox.setStyleSheet(self.checkboxStyle)
        self.equalCheckBox.stateChanged.connect(self.uncheckOthers)

        # number textbox for conditional analysis
        self.conditionalAnalysisTextBox = QLineEdit()
        self.conditionalAnalysisTextBox.setPlaceholderText('Enter Number For Conditional Analysis')
        self.conditionalAnalysisTextBox.setStyleSheet(self.lineEditStyle)
        self.conditionalAnalysisTextBox.setValidator(QtGui.QDoubleValidator().setNotation(QtGui.QDoubleValidator.Notation.StandardNotation))
        
        # add separator line
        self.line6 = QWidget()
        self.line6.setFixedHeight(1)
        self.line6.setStyleSheet("""
                    background-color: black;
                    color: black;
                    border: none;
                    padding: 3px;
                    margin: 2px;
                    """)
        
        # add Delta Threshold Detection number textbox
        self.deltaThresholdDetectionTextBox = QLineEdit()
        self.deltaThresholdDetectionTextBox.setPlaceholderText('Enter Number For Delta Threshold Detection')
        self.deltaThresholdDetectionTextBox.setStyleSheet(self.lineEditStyle)
        self.deltaThresholdDetectionTextBox.setValidator(QtGui.QDoubleValidator().setNotation(QtGui.QDoubleValidator.Notation.StandardNotation))
        
        # add Delta Threshold Detection button
        self.deltaThresholdDetectionCheckBox = QCheckBox('Delta Threshold Detection')
        self.deltaThresholdDetectionCheckBox.setChecked(False)
        self.deltaThresholdDetectionCheckBox.setStyleSheet(self.checkboxStyle)
        self.deltaThresholdDetectionCheckBox.stateChanged.connect(self.uncheckOthers)
        

        # Layout ayarı
        self.conditionalAnalysisLayout = QVBoxLayout()
        self.conditionalAnalysisLayout.addWidget(self.conditionalAnalysisTextBox)
        self.conditionalAnalysisLayout.addWidget(self.lessThanCheckBox)
        self.conditionalAnalysisLayout.addWidget(self.greaterThanCheckBox)
        self.conditionalAnalysisLayout.addWidget(self.lessThanEqualCheckBox)
        self.conditionalAnalysisLayout.addWidget(self.greaterThanEqualCheckBox)
        self.conditionalAnalysisLayout.addWidget(self.equalCheckBox)
        self.conditionalAnalysisLayout.addWidget(self.line6)
        self.conditionalAnalysisLayout.addWidget(self.deltaThresholdDetectionTextBox)
        self.conditionalAnalysisLayout.addWidget(self.deltaThresholdDetectionCheckBox)
        

        self.conditionalAnalysisWidget.setLayout(self.conditionalAnalysisLayout)
        self.conditionalAnalysisWidget.setWindowIcon(QtGui.QIcon('icon.ico'))
        
        # add "AND", "OR" checkbox for programmer analysis
        self.andCheckBox = QCheckBox('AND')
        self.andCheckBox.setChecked(False)
        self.andCheckBox.setStyleSheet(self.checkboxStyle)
        self.andCheckBox.stateChanged.connect(self.uncheckOthers)
        
        self.orCheckBox = QCheckBox('OR')
        self.orCheckBox.setChecked(False)
        self.orCheckBox.setStyleSheet(self.checkboxStyle)
        self.orCheckBox.stateChanged.connect(self.uncheckOthers)
        
        # add separator line
        self.line7 = QWidget()
        self.line7.setFixedHeight(1)
        self.line7.setStyleSheet("""
                    background-color: black;
                    color: black;
                    border: none;
                    padding: 3px;
                    margin: 2px;
                    """)
        
        # add "AND", "OR" checkbox for programmer analysis
        self.programmerAnalysisTextBox = QLineEdit()
        self.programmerAnalysisTextBox.setPlaceholderText('Enter Number For Programmer Analysis')
        self.programmerAnalysisTextBox.setStyleSheet(self.lineEditStyle)
        self.programmerAnalysisTextBox.setValidator(QtGui.QDoubleValidator().setNotation(QtGui.QDoubleValidator.Notation.StandardNotation))
        
        # add separator line
        self.line8 = QWidget()
        self.line8.setFixedHeight(1)
        self.line8.setStyleSheet("""
                    background-color: black;
                    color: black;
                    border: none;
                    padding: 3px;
                    margin: 2px;
                    """)
        
        # add "AND", "OR" checkbox for programmer analysis
        self.programmerAnalysisLayout = QVBoxLayout()
        self.programmerAnalysisLayout.addWidget(self.programmerAnalysisTextBox)
        self.programmerAnalysisLayout.addWidget(self.andCheckBox)
        self.programmerAnalysisLayout.addWidget(self.orCheckBox)
        self.programmerAnalysisLayout.addWidget(self.line8)
        
        self.programmerAnalysisWidget.setLayout(self.programmerAnalysisLayout)
        self.programmerAnalysisWidget.setWindowIcon(QtGui.QIcon('icon.ico'))
        
        

    def uncheckOthers(self, state):
        sender = self.sender()
        checkboxes = [
            self.lessThanCheckBox,
            self.greaterThanCheckBox,
            self.lessThanEqualCheckBox,
            self.greaterThanEqualCheckBox,
            self.equalCheckBox,
            self.deltaThresholdDetectionCheckBox,
            self.andCheckBox,
            self.orCheckBox,
        ]

        if state == 2: 
            for checkbox in checkboxes:
                if checkbox != sender:
                    checkbox.setChecked(False)

    def search(self):
        search_text = self.searchField.text()

        search_text = search_text.lower()
        find_count = 0

        for i, title in enumerate(self.titlesFromCSVFile):
            self.toggle_title_button_visibility(i, False)

            if search_text in title.lower():
                find_count += 1
                self.toggle_title_button_visibility(i, True)

        if find_count == 0:
            self.show_warning_and_display_all_titles('No results')

    def toggle_title_button_visibility(self, index, visible):
        title_button = self.scrollbar.widget().layout().itemAt(index).widget()
        if visible:
            title_button.show()
        else:
            title_button.hide()

    def show_warning_and_display_all_titles(self, warning_text):
        QMessageBox.warning(self, 'Error', warning_text)
        for i in range(len(self.titlesFromCSVFile)):
            self.toggle_title_button_visibility(i, True)

    def about(self):
        QMessageBox.about(self, "About CSV Reader",
                          "CSV Reader " + self.version + "\n\nAuthor: Ahmet Yasin CIVAN \n\nContact: civan.ahmetyasin@gmail.com \n\nDate: 2021-06-07 \n\nVersion: " + self.version + "\n\nDescription: This application reads csv file and draws graph with matplotlib \n\nGithub: link \n\nLicense: MIT License \n\n")
        
    def thanks(self):
        QMessageBox.about(self, "Thanks", "\n\nThanks to my friends for their support \n\nYunus AS \n\nMert Serhat SARIHAN \n\nEtka GÖKBEL \n\nÖmer KIVRAK \n\n")
        
    def help(self):
        QMessageBox.about(self, "Help", " if mouse right click on the title, draw on the same graph\n\n if you want to see FFT graph, you must enter sample rate\n\n if you want to see mean value on the graph, you must check mean on checkbox\n\n if you want to open raw data in table, you must check open raw data in table checkbox\n\n if you want to use start and end point, you must check use start and end point checkbox\n\n if you want to use math calculation, you must enter number and check + - * / checkbox")

    # def filter(self):
        # QMessageBox.about(self, "Filters", "Coming Soon \n\n like this: \n\n low pass filter \n\n high pass filter \n\n band pass filter \n\n band stop filter \n\n")

     
    def setSeparator(self):
        # q message box get data
        self.separator = self.slipLineCharacter
        self.separator, okPressed = QInputDialog.getText(
            self, "Set Separator", "Separator:" , QLineEdit.EchoMode.Normal, self.slipLineCharacter)
        
        if okPressed and self.separator != '':
            self.slipLineCharacter = self.separator


    def read_csv(self):
        
        # clear table   
        self.reviewNoteRichtextBox.clearContents()
        self.reviewNoteRichtextBox.setRowCount(100)
        self.reviewNoteRichtextBox.setItem(0, 0, QTableWidgetItem(''))
        

        if self.layout.count() > 11:
            for i in reversed(range(11, self.layout.count())):
                self.layout.itemAt(i).widget().setParent(None)

        if os.path.exists('CSV_reader_Config/file_path.yaml'):
            with open('CSV_reader_Config/file_path.yaml', 'r') as f:
                self.pathCSV = yaml.load(f, Loader=yaml.FullLoader)

        if self.pathCSV == '':
            self.pathCSV = os.getcwd()

        file_name = QFileDialog.getOpenFileName(
            self, 'Open file', self.pathCSV, 'CSV files (*.csv);;All files (*.*)')[0]
        self.selectedPath = file_name


        newTitle = file_name.split("/")
        self.CSV_file_name = newTitle[len(newTitle)-1]
        self.setWindowTitle(self.CSV_file_name)

        # Dosyanın bulunduğu klasör
        directory = "CSV_reader_Config"

        if file_name:

            self.searchField.setStyleSheet("""
                QLineEdit {
                    background-color: #FAFAFA;
                    color: #808080;
                    border-style: solid;
                    border-width: 1px;
                    border-color: #1E1E1E;
                    border-radius: 5px;
                    font: bold 14px;
                    padding: 3px;
                    margin: 2px;
                }
                QLineEdit:hover {
                    background-color: #FAFAFA;
                    color: black;
                }
                QLineEdit:focus {
                    background-color: #FAFAFA;
                    color: black;
                    border: 2px solid #777;
                }
            """)

            if not os.path.exists(directory):
                os.makedirs(directory)

            with open('CSV_reader_Config/file_path.yaml', 'w') as f:
                yaml.dump(file_name, f)

            self.searchField.setDisabled(False)

            self.lines = read_from_csv(file_name)

            # read titles from csv file
            self.titlesFromCSVFile = self.lines[0].split(self.slipLineCharacter)

            # create scroll area
            self.scrollbar = QScrollArea()
            self.scrollbar.setWidgetResizable(True)
            self.scrollbar.setWidget(QWidget())
            self.scrollbar.widget().setLayout(QVBoxLayout())
            self.scrollbar.widget().layout().setContentsMargins(0, 0, 0, 0)
            self.scrollbar.widget().layout().setSpacing(0)

            self.layout.addWidget(self.scrollbar)

            # change window size
            self.resize(500, 650)
            self.conditionalAnalysisWidget.move(810, 30)
            self.programmerAnalysisWidget.move(810, 375)

            button_count = 0

            for title in self.titlesFromCSVFile:
                # add search field for each title
                self.titleButton = MouseClickButton(title)

                if button_count % 2 == 0:
                    # set E5F9DB color for each title button
                    self.titleButton.setStyleSheet("""
                        QPushButton {
                            background-color: #E5F9DB;
                            color: black;
                            border-style: solid;
                            border-width: 1px;
                            border-color: #BBCCB4;
                            border-radius: 10px;
                            font: bold 14px;
                            padding: 3px;
                            margin: 2px;
                        }
                        QPushButton:hover {
                            background-color: #1E1E1E;
                            color: #6ECC78;
                            border-color: #777;
                        }
                    """)

                else:
                    # F0FAFA
                    self.titleButton.setStyleSheet("""
                        QPushButton {
                            background-color: #F0FAFA;
                            color: black;
                            border-style: solid;
                            border-width: 1px;
                            border-color: #C4CCCC;
                            border-radius: 10px;
                            font: bold 14px;
                            padding: 3px;
                            margin: 2px;
                        }
                        QPushButton:hover {
                            background-color: #1E1E1E;
                            color: #6ECC78;
                            border-color: #777;
                        }
                    """)

                self.titleButton.clicked.connect(self.show_title)
                # add to scrollbar each title button
                self.scrollbar.widget().layout().addWidget(self.titleButton)

                button_count += 1
                
                # add review notes to table from yaml file
                        #split file name
                newTitle = self.CSV_file_name.split(".")
                yaml_file_name = newTitle[0]
                
                #split path
                rawPath = self.selectedPath.split("/")

                for i in range(0, len(rawPath)-1):
                    if i == 0:
                        path = rawPath[i]
                    else:
                        path = path + '/' + rawPath[i]
                
                if os.path.exists(path + '/' + yaml_file_name + '.yaml'):
                    with open(path + '/' + yaml_file_name + '.yaml', 'r') as f:
                        review_note = yaml.load(f, Loader=yaml.FullLoader)
                        for key, value in review_note.items():
                            self.reviewNoteRichtextBox.setItem(key, 0, QTableWidgetItem(value))
                                            
                

        else:
            # change window size
            self.resize(300, 300)
            self.searchField.setDisabled(True)
            QMessageBox.warning(self, 'Error', 'No file selected')

    def review_note_save(self):
        
        if self.selectedPath == '':
            QMessageBox.warning(self, 'Error', 'No file selected')
            return

        if self.CSV_file_name == '':
            QMessageBox.warning(self, 'Error', 'No file selected')
            return

        if self.reviewNoteRichtextBox.item(0, 0) == None:
            QMessageBox.warning(self, 'Error', 'No review note')
            return
        
 
        review_note = {}
        counter = 0

        for i in range(0, 100):
            # get review note from table
            if self.reviewNoteRichtextBox.item(i, 0) != None:
                review_note[counter] = self.reviewNoteRichtextBox.item(i, 0).text()
                counter += 1
            
        #split file name
        newTitle = self.CSV_file_name.split(".cs")
        yaml_file_name = newTitle[0]
        
        #split path
        rawPath = self.selectedPath.split("/")

        for i in range(0, len(rawPath)-1):
            if i == 0:
                path = rawPath[i]
            else:
                path = path + '/' + rawPath[i]        
                
        if not os.path.exists(path + '/' + yaml_file_name+ '.yaml'):
            print('not exist')
            print(path + '/' + yaml_file_name + '.yaml')
            with open(path + '/' + yaml_file_name + '.yaml', 'w') as f:
                yaml.dump(review_note, f)
        else:
            print('exist')
            print(path + '/' + yaml_file_name + '.yaml')
            with open(path + '/' + yaml_file_name + '.yaml', 'a') as f:
                #clear file
                f.seek(0)
                f.truncate()
                yaml.dump(review_note, f)

        QMessageBox.about(self, "Review Note", "Review Saved")        
        
        


    def show_title(self, mouseEvent):

        self.same_graph = False

        if mouseEvent == "right":
            self.same_graph = True

        self.flight_mode_column = []
        self.fmode = True

        # detect title column
        for i in range(len(self.titlesFromCSVFile)):
            if "ap_flight_mode" == self.titlesFromCSVFile[i] or "flightMode" == self.titlesFromCSVFile[i] or "flight_mode" == self.titlesFromCSVFile[i]:
                self.flight_mode_column = i

                # if all flight mode column is zero, disable flight mode
                for j in range(1, len(self.lines)):
                    if self.lines[j].split(self.slipLineCharacter)[self.flight_mode_column] != '0':
                        self.fmode = True
                        break
                    else:
                        self.fmode = False

                break
            else:
                self.fmode = False

        # detect title column
        for i in range(len(self.titlesFromCSVFile)):
            if self.sender().text() == self.titlesFromCSVFile[i]:
                self.column = i
                break

        # check start and end point is digit or range is valid or not
        if self.startEndPointCheckBox.isChecked():
            if self.startPoint.text().isdigit() and self.endPoint.text().isdigit() and int(self.startPoint.text()) < int(self.endPoint.text()) and int(self.startPoint.text()) >= 0 and int(self.endPoint.text()) <= len(self.lines):
                pass
            else:
                self.startPoint.setText('')
                self.endPoint.setText('')
                self.startEndPointCheckBox.setChecked(False)
                # set message box
                msg = QMessageBox()
                msg.setText(
                    "Start and End Point is not valid or range is not valid")
                msg.setWindowTitle("Error")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec()
                return

        # draw line graph with matplotlib
        self.draw_line_graph(self.lines, self.column,
                             self.fmode, self.sender().text())

    def draw_line_graph(self, lines, column, doesHaveFmode, lineName):
        # read data from csv file
        data = []
        point = 0.0

        if  self.plusCheckBox.isChecked() or self.minusCheckBox.isChecked() or self.multiplyCheckBox.isChecked() or self.divideCheckBox.isChecked():
            self.mathCalculationTextBox.setText(self.mathCalculationTextBox.text().replace(',', '.'))
            if self.mathCalculationTextBox.text().replace('.', '', 1).isdigit() and self.mathCalculationTextBox.text() != '':
                pass
            else:
                self.mathCalculationTextBox.setText('')
                # set message box
                msg = QMessageBox()
                msg.setText("Math Calculation is not valid")
                msg.setWindowTitle("Error")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec()
                return

        if not doesHaveFmode:
            for i in range(len(lines)):
                if i != 0:
                    try:
                        if self.startEndPointCheckBox.isChecked():
                            if i >= int(self.startPoint.text()) and i <= int(self.endPoint.text()):
                                point = float(lines[i].split(
                                    self.slipLineCharacter)[column].replace(',', '.'))
                                # get mathCalculationTextBox float value
                                if self.plusCheckBox.isChecked():
                                    point = point + \
                                        float(self.mathCalculationTextBox.text())
                                if self.minusCheckBox.isChecked():
                                    point = point - \
                                        float(self.mathCalculationTextBox.text())
                                if self.multiplyCheckBox.isChecked():
                                    point = point * \
                                        float(self.mathCalculationTextBox.text())
                                if self.divideCheckBox.isChecked():
                                    point = point / \
                                        float(self.mathCalculationTextBox.text())

                                data.append(point)
                        else:
                            point = float(lines[i].split(
                                self.slipLineCharacter)[column].replace(',', '.'))
                            # get mathCalculationTextBox float value
                            if self.plusCheckBox.isChecked():
                                point = point + \
                                    float(self.mathCalculationTextBox.text())
                            if self.minusCheckBox.isChecked():
                                point = point - \
                                    float(self.mathCalculationTextBox.text())
                            if self.multiplyCheckBox.isChecked():
                                point = point * \
                                    float(self.mathCalculationTextBox.text())
                            if self.divideCheckBox.isChecked():
                                point = point / \
                                    float(self.mathCalculationTextBox.text())

                            data.append(point)
                    except:
                        pass

        else:
            for i in range(len(lines)):
                if i != 0:
                    try:
                        if int(lines[i].split(self.slipLineCharacter)[
                                self.flight_mode_column].replace(',', '.')) != 0:
                            self.counter_for_flight_mode += 1
                            if self.startEndPointCheckBox.isChecked():
                                if self.counter_for_flight_mode >= int(self.startPoint.text()) and self.counter_for_flight_mode <= int(self.endPoint.text()):
                                    point = float(lines[i].split(
                                        self.slipLineCharacter)[column].replace(',', '.'))

                                    if self.plusCheckBox.isChecked():
                                        point = point + \
                                            float(
                                                self.mathCalculationTextBox.text())
                                    if self.minusCheckBox.isChecked():
                                        point = point - \
                                            float(
                                                self.mathCalculationTextBox.text())
                                    if self.multiplyCheckBox.isChecked():
                                        point = point * \
                                            float(
                                                self.mathCalculationTextBox.text())
                                    if self.divideCheckBox.isChecked():
                                        point = point / \
                                            float(
                                                self.mathCalculationTextBox.text())
                                    data.append(point)
                            else:
                                point = float(lines[i].split(
                                    self.slipLineCharacter)[column].replace(',', '.'))

                                if self.plusCheckBox.isChecked():
                                    point = point + \
                                        float(
                                            self.mathCalculationTextBox.text())
                                if self.minusCheckBox.isChecked():
                                    point = point - \
                                        float(
                                            self.mathCalculationTextBox.text())
                                if self.multiplyCheckBox.isChecked():
                                    point = point * \
                                        float(
                                            self.mathCalculationTextBox.text())
                                if self.divideCheckBox.isChecked():
                                    point = point / \
                                        float(
                                            self.mathCalculationTextBox.text())
                                data.append(point)

                        if len(self.flight_mode_column) == 0:
                            if self.startEndPointCheckBox.isChecked():
                                if i >= int(self.startPoint.text()) and i <= int(self.endPoint.text()):
                                    if self.plusCheckBox.isChecked():
                                        point = point + \
                                            float(
                                                self.mathCalculationTextBox.text())
                                    if self.minusCheckBox.isChecked():
                                        point = point - \
                                            float(
                                                self.mathCalculationTextBox.text())
                                    if self.multiplyCheckBox.isChecked():
                                        point = point * \
                                            float(
                                                self.mathCalculationTextBox.text())
                                    if self.divideCheckBox.isChecked():
                                        point = point / \
                                            float(
                                                self.mathCalculationTextBox.text())
                                    data.append(point)                        
                            else:
                                if self.plusCheckBox.isChecked():
                                    point = point + \
                                        float(
                                            self.mathCalculationTextBox.text())
                                if self.minusCheckBox.isChecked():
                                    point = point - \
                                        float(
                                            self.mathCalculationTextBox.text())
                                if self.multiplyCheckBox.isChecked():
                                    point = point * \
                                        float(
                                            self.mathCalculationTextBox.text())
                                if self.divideCheckBox.isChecked():
                                    point = point / \
                                        float(
                                            self.mathCalculationTextBox.text())
                                data.append(point)

                    except:
                        pass

        self.label_name = self.sender().text()
        self.counter_for_flight_mode = 0

        if self.multipleTwoLineCheckBox.isChecked(): 
            if(self.dataOneOn == False):
                self.data_selected_one = data
                self.dataOneOn = True
                self.buttonStyle = self.sender().styleSheet()
                self.qButton = self.sender()
               
                #change color selection button
                self.sender().setStyleSheet("""
                    QPushButton {
                        background-color: #6ECC78;
                        color: black;
                        border-style: solid;
                        border-width: 1px;
                        border-color: #1E1E1E;
                        border-radius: 10px;
                        font: bold 14px;
                        padding: 3px;
                        margin: 2px;
                    }
                    QPushButton:hover {
                        background-color: #1E1E1E;
                        color: #6ECC78;
                        border-color: #777;
                    }
                """)
                return
                                
            elif(self.dataOneOn == True and self.dataTwoOn == False):
                self.data_selected_two  = data
                self.dataTwoOn = True

            if self.dataOneOn == True and self.dataTwoOn == True:            
                try:
                    data = np.multiply(self.data_selected_one, self.data_selected_two)
                    self.dataOneOn = False
                    self.dataTwoOn = False
                    self.qButton.setStyleSheet(self.buttonStyle)
                    self.multipleTwoLineCheckBox.setChecked(False)
                    
                    if self.multipleLineLabel.text() == '':
                        self.multipleLineLabel.setText("Multiple Two Line")
                    
                    self.label_name = self.multipleLineLabel.text()

                except:
                    self.dataOneOn = False
                    self.dataTwoOn = False
                    self.multipleTwoLineCheckBox.setChecked(False)
                    QMessageBox.about(self, "Error", "Multiple Line Error")
                    return

        if (self.movingAverageCheckBox.isChecked() and not self.movingAveragePeriod.text().isdigit()) or (self.movingAverageCheckBox.isChecked() and self.movingAveragePeriod.text() == ''):
            msg = QMessageBox()
            msg.setText(
                "If you want to see Moving Average graph, you must enter period!")
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()
            self.movingAverageCheckBox.setChecked(False)

        if (self.drawOnTheSameGraphCheckBox.isChecked() or self.same_graph) and (self.lineCounter >= 1 and lineName == self.sender().text()):
            if self.yAxisTwinxCheckBox.isChecked():
                self.ax2 = self.ax.twinx()
                self.OnTheSameGraphCounter += 1
                self.twinGraphCounter += 1

                self.ax2.plot(data, label=self.label_name,
                              linewidth=1.0, color=self.colors[self.lineCounter % len(self.colors)])

                # write label under to the line
                self.ax2.annotate(self.label_name, xy=(-10, data[0]), xytext=(
                    -10, data[0] - 0.1), color=self.colors[self.lineCounter % len(self.colors)])

                # write label on the line

                if self.meanCheckBox.isChecked():
                    mean_value = np.mean(data)

                    meanLabel = self.label_name + \
                        f' Mean: {mean_value:.2f} '

                    self.ax2.axhline(y=mean_value, color=self.colors[self.lineCounter % len(self.colors)],
                                     linestyle='--', label=meanLabel)
                
                if self.movingAverageCheckBox.isChecked():
                    moving_average_data = np.convolve(data, np.ones(int(self.movingAveragePeriod.text()))/int(self.movingAveragePeriod.text()), mode='valid')
                    movingAverageLabel = self.label_name + ' Moving Average' + ', Period: ' + self.movingAveragePeriod.text()
                    try:
                        self.ax.plot(moving_average_data, label=movingAverageLabel ,
                                  linestyle='--', color='black')
                    except:
                        QMessageBox.about(self, "Error", "Moving Average Error")

                self.ax2.set_ylabel(self.label_name, color=self.colors[self.lineCounter % len(
                    self.colors)], labelpad=10 * self.OnTheSameGraphCounter)

                self.ax2.tick_params(
                    'y', colors=self.colors[self.lineCounter % len(self.colors)])

                self.ax2.legend(loc='upper right')
            else:
                self.OnTheSameGraphCounter += 1

                self.ax.plot(data, label=self.label_name, linewidth=1, color=self.colors[self.lineCounter % len(self.colors)])

                if self.meanCheckBox.isChecked():
                    mean_value = np.mean(data)

                    meanLabel = self.label_name + \
                        f' Mean: {mean_value:.2f} '

                    self.ax.axhline(y=mean_value, color=self.colors[self.lineCounter % len(self.colors)],
                                    linestyle='--', label=meanLabel)
                
                if self.movingAverageCheckBox.isChecked():
                    moving_average_data = np.convolve(data, np.ones(int(self.movingAveragePeriod.text()))/int(self.movingAveragePeriod.text()), mode='valid')
                    movingAverageLabel = self.label_name + ' Moving Average' + ', Period: ' + self.movingAveragePeriod.text()
                    try:
                        self.ax.plot(moving_average_data, label=movingAverageLabel,
                                  linestyle='--', color='black')
                    except:
                        QMessageBox.about(self, "Error", "Moving Average Error")

                self.ax.legend(loc='upper left')

                self.ax_title = self.ax_title + ", " + self.label_name

                self.ax.set_title(self.ax_title)
                plt.get_current_fig_manager().set_window_title(
                    self.CSV_file_name + " / " + self.ax_title)

            self.fig.canvas.draw()

            title = str(self.titleList[len(self.titleList)-1])
            self.titleList.pop(len(self.titleList)-1)
            self.titleList.append(title)

        else:
            if lineName == self.sender().text():
                self.OnTheSameGraphCounter = 0
                self.twinGraphCounter = 0

                self.fig, self.ax = plt.subplots()

                self.ax.set_title(self.label_name)

                self.fig.canvas.mpl_connect(
                    'close_event', self.close_fig_event)

                self.ax.plot(
                    data, label=self.label_name, linewidth=1, color='blue')
                self.ax.grid(True)
                self.ax.set_xlabel('Sample number')
                self.ax.set_ylabel('Value')

                if self.meanCheckBox.isChecked():
                    mean_value = np.mean(data)

                    meanLabel = self.label_name + \
                        f' Mean: {mean_value:.2f} '

                    self.ax.axhline(y=mean_value, color='blue',
                                    linestyle='--', label=meanLabel)

                if self.movingAverageCheckBox.isChecked():
                    moving_average_data = np.convolve(data, np.ones(int(self.movingAveragePeriod.text()))/int(self.movingAveragePeriod.text()), mode='valid')
                    movingAverageLabel = self.label_name + ' Moving Average' + ', Period: ' + self.movingAveragePeriod.text()
                    try:
                        self.ax.plot(moving_average_data, label=movingAverageLabel ,
                                  linestyle='--', color='black')
                    except:
                        QMessageBox.about(self, "Error", "Moving Average Error")

                self.ax.legend(loc='upper left')

                title = str(self.sender().text())

                self.titleList.append(title)

                plt.show()

                self.ax_title = self.sender().text()
                plt.get_current_fig_manager().set_window_title(
                    self.CSV_file_name + " / " + self.ax_title)

                self.lineCounter = 0

        if self.fftCheckBox.isChecked() and (not self.fftFrequency.text().isdigit() or self.fftFrequency.text() == ''):
            msg = QMessageBox()
            msg.setText(
                "If you want to see FFT graph, you must enter sample rate!")
            msg.setWindowTitle("Error")
            msg.exec()

        if self.fftCheckBox.isChecked() and self.fftFrequency.text() != '' and self.fftFrequency.text().isdigit():
            # get sample rate from label text
            Fs = int(self.fftFrequency.text())
            T = 1 / Fs  # Örnekleme periyodu (s)
            L = len(data)  # Sinyal uzunluğu (örnek sayısı)
            t = np.arange(0, L) * T  # Zaman vektörü

            # Verileri NumPy dizisine dönüştürme
            sinyal = np.array(data)

            # FFT hesaplama
            fft = np.fft.fft(sinyal)
            frekanslar = np.fft.fftfreq(L, T)[:L // 2]

            # FFT grafiği
            plt.figure()
            plt.grid(True)
            plt.plot(frekanslar, 2 / L * np.abs(fft[:L // 2]))
            plt.xlabel('Frekans (Hz)')
            plt.ylabel('Amplitüd')
            plt.title(self.sender().text() + ' FFT')
            plt.show()

        if self.openRawData.isChecked():

            # if same draw same graph, add new table
            if not self.drawOnTheSameGraphCheckBox.isChecked() and not self.same_graph:
                self.tableColumnCounter = 0
                self.rawDataWidget = QWidget()
                self.rawDataWidget.setWindowTitle(
                    self.label_name + " Raw Data")
                self.rawDataWidget.resize(500, 500)
                self.rawDataWidget.show()
                self.layout = QVBoxLayout()
                
                self.exportButton = QPushButton( self.label_name + ' ' + 'Export as Cpp Array' )
                
                # print to console as uint16_t c array without .0
                self.CppArrayData = "uint16_t " + self.label_name + "[] = {"
                for i in range(len(data)):
                    if i == len(data)-1:
                        self.CppArrayData = self.CppArrayData + str(int(data[i]))
                    else:
                        self.CppArrayData = self.CppArrayData + str(int(data[i])) + ", "
                self.CppArrayData = self.CppArrayData + "};"

                self.exportButton.clicked.connect(self.export_as_cpp_array)
                self.layout.addWidget(self.exportButton)

                self.table = QTableWidget()

                self.table.setColumnCount(1)
                self.table.setRowCount(len(data))

                # add data to table
                for i in range(len(data)):
                    self.table.setItem(i, 0, QTableWidgetItem(str(data[i])))

                # set table header
                self.table.setHorizontalHeaderLabels([self.label_name])

                self.layout.addWidget(self.table)
                self.rawDataWidget.setLayout(self.layout)
            else:
                if not self.rawDataWidget.isVisible():
                    self.tableColumnCounter = 0
                    self.rawDataWidget = QWidget()
                    self.rawDataWidget.setWindowTitle(
                        self.label_name + " Raw Data")
                    self.rawDataWidget.resize(500, 500)
                    self.rawDataWidget.show()
                    self.layout = QVBoxLayout()
                    self.table = QTableWidget()
                    self.table.setColumnCount(1)
                    self.table.setRowCount(len(data))

                    # add data to table
                    for i in range(len(data)):
                        self.table.setItem(
                            i, 0, QTableWidgetItem(str(data[i])))

                    # set table header
                    self.table.setHorizontalHeaderLabels(
                        [self.label_name])

                    self.layout.addWidget(self.table)
                    self.rawDataWidget.setLayout(self.layout)
                else:
                    self.tableColumnCounter += 1

                    # if draw on the same graph, add same table as column
                    self.table.setColumnCount(self.tableColumnCounter + 1)
                    self.table.setRowCount(len(data))

                    # add data to table
                    for i in range(len(data)):
                        self.table.setItem(i, self.tableColumnCounter,
                                           QTableWidgetItem(str(data[i])))
                    # set column header name as line name
                    self.table.setHorizontalHeaderItem(
                        self.tableColumnCounter, QTableWidgetItem(self.label_name))
        
        if self.conditionalAnalysisTextBox.text() != '' and not self.lessThanCheckBox.isChecked() and not self.greaterThanCheckBox.isChecked() and not self.lessThanEqualCheckBox.isChecked() and not self.greaterThanEqualCheckBox.isChecked() and not self.equalCheckBox.isChecked():
            msg = QMessageBox()
            msg.setText(
                "If you want to use conditional analysis, you must check one of the checkbox!")
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()
          
        if self.conditionalAnalysisTextBox.text() != '' and (self.lessThanCheckBox.isChecked() or self.greaterThanCheckBox.isChecked() or self.lessThanEqualCheckBox.isChecked() or self.greaterThanEqualCheckBox.isChecked() or self.equalCheckBox.isChecked()):
            
            # get number from line edit
            number = self.conditionalAnalysisTextBox.text()
            number = number.replace(',', '.')
            
            if number.isdigit():
                number = int(number)
            else:
                number = float(number)
            
            conditionalData = []
            sampleNumberData = []

            # check checkbox is checked or not
            if self.lessThanCheckBox.isChecked():
                for i in range(len(data)):
                    if data[i] < number:
                        conditionalData.append(data[i])
                        sampleNumberData.append(i)
                        
            elif self.greaterThanCheckBox.isChecked():
                for i in range(len(data)):
                    if data[i] > number:
                        conditionalData.append(data[i])
                        sampleNumberData.append(i)
                    
            elif self.lessThanEqualCheckBox.isChecked():
                for i in range(len(data)):
                    if data[i] <= number:
                        conditionalData.append(data[i])
                        sampleNumberData.append(i)
                    
            elif self.greaterThanEqualCheckBox.isChecked():
                for i in range(len(data)):
                    if data[i] >= number:
                        conditionalData.append(data[i])
                        sampleNumberData.append(i)
                        msg = QMessageBox()
                    
            elif self.equalCheckBox.isChecked():
                for i in range(len(data)):
                    if data[i] == number:
                        conditionalData.append(data[i])
                        sampleNumberData.append(i)
            
            if len(conditionalData) == 0 and len(sampleNumberData) == 0:
                msg = QMessageBox()
                msg.setText(
                    "There is no data detected with conditional analysis!")
                msg.setWindowTitle("Error")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec()
            else:           
                # new table for conditional analysis
                self.rawDataWidget = QWidget()
                self.rawDataWidget.setWindowTitle(
                    self.label_name + " Conditional Analysis")
                self.rawDataWidget.resize(500, 500)
                self.rawDataWidget.show()
                self.layout = QVBoxLayout()
                self.table = QTableWidget()
                self.table.setColumnCount(2)
                self.table.setRowCount(len(conditionalData))
                self.table.setHorizontalHeaderLabels(['Sample Number', 'Sample Value' + ' ' + self.label_name])
                
                # add information lable for conditional analysis
                self.conditionalAnalysisLabel = QLabel()
                self.conditionalAnalysisLabel.setText(f"Detected {len(conditionalData)} data is detected")
                
                # add max value to table
                self.maxValue = QLabel()
                self.maxValue.setText(f"Max Value: {max(conditionalData)}" + ', ' + 'Sample Number: ' + str(sampleNumberData[conditionalData.index(max(conditionalData))]))
                
                # add min value to table
                self.minValue = QLabel()
                self.minValue.setText(f"Min Value: {min(conditionalData)}" + ', ' + 'Sample Number: ' + str(sampleNumberData[conditionalData.index(min(conditionalData))]))
                
                # add mean value to table
                self.meanValue = QLabel()
                self.meanValue.setText(f"Mean Value: {np.mean(conditionalData):.3f}")
                
                # add about button for conditional analysis
                self.conditionalAnalysisAbout = QPushButton("About")
                self.conditionalAnalysisAbout.clicked.connect(self.conditional_analysis_about)
                
                # add data to table
                for i in range(len(conditionalData)):
                    self.table.setItem(i, 0, QTableWidgetItem(str(sampleNumberData[i])))
                    self.table.setItem(i, 1, QTableWidgetItem(str(conditionalData[i])))
                
                # set table header
                self.layout.addWidget(self.conditionalAnalysisLabel)
                self.layout.addWidget(self.maxValue)
                self.layout.addWidget(self.minValue)
                self.layout.addWidget(self.meanValue)
                self.layout.addWidget(self.conditionalAnalysisAbout)
                self.layout.addWidget(self.table)
                self.rawDataWidget.setLayout(self.layout)
        
        if self.deltaThresholdDetectionTextBox.text() == '' and self.deltaThresholdDetectionCheckBox.isChecked():
            msg = QMessageBox()
            msg.setText(
                "If you want to use delta threshold detection, you must enter number!")
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()
        
        if self.deltaThresholdDetectionCheckBox.isChecked() and self.deltaThresholdDetectionTextBox.text() != '':
            # get number from line edit
            number = self.deltaThresholdDetectionTextBox.text()
            number = number.replace(',', '.')
            
            if number.isdigit():
                number = int(number)
            else:
                number = float(number)
            
            deltaData = []
            sampleNumberData = []
            calculatedDeltaData = []

            # jump first data            
            for i in range(1, len(data)):

                if abs(data[i] - data[i-1]) > number:
                    calculatedDeltaData.append(abs(data[i] - data[i-1]))
                    calculatedDeltaData.append(abs(data[i] - data[i-1]))
                    deltaData.append(data[i-1])
                    deltaData.append(data[i])
                    sampleNumberData.append(i-1)
                    sampleNumberData.append(i)
                       
            if len(deltaData) > 0 and len(sampleNumberData) > 0 :
                # new table for delta threshold detection
                self.rawDataWidget = QWidget()
                self.rawDataWidget.setWindowTitle(
                    self.label_name + " Delta Threshold Detection")
                self.rawDataWidget.resize(500, 500)
                self.rawDataWidget.show()
                self.layout = QVBoxLayout()
                self.table = QTableWidget()
                self.table.setColumnCount(3)
                self.table.setRowCount(len(deltaData))
                self.table.setHorizontalHeaderLabels(['Sample Number', 'Sample Value' + ' ' + self.label_name, 'Calculated Delta'])
                                    
                # add data to table
                for i in range(len(deltaData)):
                    self.table.setItem(i, 0, QTableWidgetItem(str(sampleNumberData[i])))
                    self.table.setItem(i, 1, QTableWidgetItem(str(deltaData[i])))
                    self.table.setItem(i, 2, QTableWidgetItem(f"{calculatedDeltaData[i]:.3f}"))
                    
                # add information lable for delta threshold detection
                self.deltaThresholdDetectionLabel = QLabel()
                self.deltaThresholdDetectionLabel.setText(f"Detected {int(len(deltaData)/2)} data is greater than {number}")
                
                # add max delta value to table
                self.maxDeltaValue = QLabel()
                self.maxDeltaValue.setText(f"Max Delta Value: {max(calculatedDeltaData):.3f}" + ', ' + 'Sample Number: ' + str(sampleNumberData[calculatedDeltaData.index(max(calculatedDeltaData))]))
                
                # add min delta value to table
                self.minDeltaValue = QLabel()
                self.minDeltaValue.setText(f"Min Delta Value: {min(calculatedDeltaData):.3f}" + ', ' + 'Sample Number: ' + str(sampleNumberData[calculatedDeltaData.index(min(calculatedDeltaData))]))
                
                # add mean delta value to table
                self.meanDeltaValue = QLabel()
                self.meanDeltaValue.setText(f"Mean Delta Value: {np.mean(calculatedDeltaData):.3f}")
                
                # add about button for delta threshold detection
                self.deltaThresholdDetectionAbout = QPushButton("About")
                self.deltaThresholdDetectionAbout.clicked.connect(self.delta_threshold_detection_about)

                
                self.layout.addWidget(self.deltaThresholdDetectionLabel)
                self.layout.addWidget(self.maxDeltaValue)
                self.layout.addWidget(self.minDeltaValue)
                self.layout.addWidget(self.meanDeltaValue)                
                self.layout.addWidget(self.deltaThresholdDetectionAbout)
                self.layout.addWidget(self.table)
                self.rawDataWidget.setLayout(self.layout)                    
            else:
                msg = QMessageBox()
                msg.setText(
                    "There is no Delta Threshold")
                msg.setWindowTitle("Info")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec()
        
        if self.programmerAnalysisTextBox.text() == '' and self.andCheckBox.isChecked() and self.orCheckBox.isChecked():
            msg = QMessageBox()
            msg.setText(
                "If you want to use programmer analysis, you must enter number!")
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()
        
        if self.programmerAnalysisTextBox.text() != '' and (self.andCheckBox.isChecked() or self.orCheckBox.isChecked()):
            # get hex number from line edit
            number = self.programmerAnalysisTextBox.text()
            
            if '0x' in number:
                number = number.replace('0x', '')

                if all(c in '0123456789ABCDEFabcdef' for c in number):
                    number = int(number, 16)  
                else:
                    msg = QMessageBox()
                    msg.setText(
                        "If you want to use programmer analysis, you must enter a valid hex number!")
                    msg.setWindowTitle("Error")
                    msg.setIcon(QMessageBox.Icon.Warning)
                    msg.exec()
                    return
            elif '0b' in number:
                number = number.replace(' ', '')
                number = number.replace('0b', '')
                if all(c in '01' for c in number):
                    number = int(number, 2)  
                else:
                    msg = QMessageBox()
                    msg.setText(
                        "If you want to use programmer analysis, you must enter a valid binary number!")
                    msg.setWindowTitle("Error")
                    msg.setIcon(QMessageBox.Icon.Warning)
                    msg.exec()
                    return            
            else:
                if number.isdigit():
                    number = int(number)  
                else:
                    msg = QMessageBox()
                    msg.setText(
                        "If you want to use programmer analysis, you must enter a valid decimal or hex number!")
                    msg.setWindowTitle("Error")
                    msg.setIcon(QMessageBox.Icon.Warning)
                    msg.exec()
                    return
            
            bitwiseData = []
            sampleNumberData = []
            
            if self.andCheckBox.isChecked():
                for i in range(len(data)):
                    bitwiseData.append(int(data[i]) & number)
                    sampleNumberData.append(i)
                    

            if self.orCheckBox.isChecked():
                for i in range(len(data)):
                    bitwiseData.append(int(data[i]) | number)
                    sampleNumberData.append(i)
            
            if len(bitwiseData) > 0  and len(sampleNumberData) > 0:
                # new table for programmer analysis
                self.rawDataWidget = QWidget()
                self.rawDataWidget.setWindowTitle(
                    self.label_name + " Programmer Analysis")
                self.rawDataWidget.resize(500, 500)
                self.rawDataWidget.show()
                self.layout = QVBoxLayout()
                self.table = QTableWidget()
                self.table.setColumnCount(4)
                self.table.setRowCount(len(sampleNumberData))
                self.table.setHorizontalHeaderLabels(['Sample Number', 'Sample Value' + ' ' + self.label_name, 'Bitwise Value', 'Binary Value'])
                
                # add data to table
                for i in range(len(sampleNumberData)):
                    self.table.setItem(i, 0, QTableWidgetItem(str(sampleNumberData[i])))
                    self.table.setItem(i, 1, QTableWidgetItem(str(data[i])))
                    self.table.setItem(i, 2, QTableWidgetItem(hex(int(bitwiseData[i]))))
                    self.table.setItem(i, 3, QTableWidgetItem(bin(int(bitwiseData[i]))))
                
                # add information lable for programmer analysis
                self.programmerAnalysisLabel = QLabel()
                self.programmerAnalysisLabel.setText(f"Detected {len(sampleNumberData)} data is detected")
                
                # add about button for programmer analysis
                self.programmerAnalysisAbout = QPushButton("About")
                self.programmerAnalysisAbout.clicked.connect(self.programmer_analysis_about)

                self.programmerAnalysisFilterButton = QPushButton("Filter Zero Value")

                self.layout.addWidget(self.programmerAnalysisLabel)
                self.layout.addWidget(self.programmerAnalysisAbout)
                self.layout.addWidget(self.programmerAnalysisFilterButton)
                self.layout.addWidget(self.table)
                self.rawDataWidget.setLayout(self.layout)
                
        
        self.lineCounter += 1

    def fftCheckBoxChanged(self):
        if self.fftCheckBox.isChecked():
            self.fftFrequency.setEnabled(True)
            self.fftFrequency.setStyleSheet("""
                QLineEdit {
                    background-color: #FAFAFA;
                    color: #808080;
                    border-style: solid;
                    border-width: 1px;
                    border-color: #1E1E1E;
                    border-radius: 5px;
                    font: bold 14px;
                    padding: 3px;
                    margin: 2px;
                }
                QLineEdit:hover {
                    background-color: #FAFAFA;
                    color: black;
                }
                QLineEdit:focus {
                    background-color: #FAFAFA;
                    color: black;
                    border: 2px solid #777;
                }
            """)
        else:
            self.fftFrequency.setEnabled(False)
            self.fftFrequency.setStyleSheet(self.lineEditStyle)

    def close_fig_event(self, event):
        counter = 0
        for title in self.titleList:
            if title == str(self.titleList[len(self.titleList)-1]):
                self.titleList.pop(counter)
                self.lineCounter = 0
            counter = counter + 1
    
    # add keyboard event for shortcut
    def keyPressEvent(self, event):
        super().keyPressEvent(event)

        if event.key() == Qt.Key.Key_Escape:
            self.mathCalculationWidget.close()
            self.filterWidget.close()
            self.reviewNoteWidget.close()
            self.conditionalAnalysisWidget.close()
            self.rawDataWidget.close()
            self.programmerAnalysisWidget.close()
        if event.key() == Qt.Key.Key_Y:
            self.yAxisTwinxCheckBox.setChecked(True)
        if event.key() == Qt.Key.Key_D:
            self.drawOnTheSameGraphCheckBox.setChecked(not self.drawOnTheSameGraphCheckBox.isChecked())
        if event.key() == Qt.Key.Key_F:
            self.fftCheckBox.setChecked(not self.fftCheckBox.isChecked())
        if event.key() == Qt.Key.Key_M:
            self.meanCheckBox.setChecked(not self.meanCheckBox.isChecked())
        if event.key() == Qt.Key.Key_R:
            self.openRawData.setChecked(not self.openRawData.isChecked())
        if event.key() == Qt.Key.Key_S:
            self.startEndPointCheckBox.setChecked(not self.startEndPointCheckBox.isChecked())
        if event.key() == Qt.Key.Key_P:
            self.plusCheckBox.setChecked(not self.plusCheckBox.isChecked())
    
    def keyReleaseEvent(self, event):
        super().keyReleaseEvent(event)
        if event.key() == Qt.Key.Key_Y:
            self.yAxisTwinxCheckBox.setChecked(False)
    
    def export_as_cpp_array(self):
        # print to .cpp file as uint16_t c array without .0
        if self.selectedPath == '':
            QMessageBox.warning(self, 'Error', 'No file selected')
            return
        
        if self.CSV_file_name == '':
            QMessageBox.warning(self, 'Error', 'No file selected')
            return
        
        if self.label_name == '':
            QMessageBox.warning(self, 'Error', 'No label name')
            return
        
        if self.CppArrayData == '':
            QMessageBox.warning(self, 'Error', 'No data')
            return
        
        
        # export self.CppArrayData to .cpp file

        #split file name
        newTitle = self.CSV_file_name.split(".cs")
        yaml_file_name = newTitle[0]
        
        #split path
        rawPath = self.selectedPath.split("/")
        for i in range(0, len(rawPath)-1):
            if i == 0:
                path = rawPath[i]
            else:
                path = path + '/' + rawPath[i]
        
        if not os.path.exists(path + '/' + yaml_file_name + '.cpp'):
            with open(path + '/' + yaml_file_name + '_Raw_Data_Array' + '.cpp', 'w') as f:
                f.write(self.CppArrayData)
        else:
            with open(path + '/' + yaml_file_name + '_Raw_Data_Array' + '.cpp', 'a') as f:
                f.write(self.CppArrayData)
        
        QMessageBox.about(self, "Export as Cpp Array", "Exported as Cpp Array")
    
    def closeEvent(self, event):
        # close all widgets
        self.mathCalculationWidget.close()
        self.filterWidget.close()
        self.reviewNoteWidget.close()
        self.conditionalAnalysisWidget.close()
        self.rawDataWidget.close()
        self.programmerAnalysisWidget.close()
        event.accept()
    
    def delta_threshold_detection_about(self):
        # show about message box for delta threshold detection
        msg = QMessageBox()
        msg.setText(
            "Delta Threshold Detection is a method that detects the difference between two consecutive data and compares it with the entered threshold value. If the difference is greater than the threshold value, the data is detected."
            "\n\n Sample Number: Detected sample number, i and i-1"
            "\n Sample Value: Detected sample value, data[i] and data[i-1]"
            "\n Calculated Delta: Calculated difference between two consecutive data, abs(data[i] - data[i-1])"
            "\n\n Formula: abs(data[i] - data[i-1]) > threshold")
        
        msg.setWindowTitle("Delta Threshold Detection")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec() 
    
    def conditional_analysis_about(self):
        # show about message box for conditional analysis
        msg = QMessageBox()
        msg.setText(
            "Conditional Analysis is a method that detects the data that meets the specified condition."
            "\n\n Sample Number: Detected sample number"
            "\n Sample Value: Detected sample value"
            "\n\n Formula: data[i] < number, data[i] > number, data[i] <= number, data[i] >= number, data[i] == number")
        
        msg.setWindowTitle("Conditional Analysis")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
     
    def programmer_analysis_about(self):
        # show about message box for programmer analysis
        msg = QMessageBox()
        msg.setText(
            "Programmer Analysis is a method that performs bitwise operations on the data."
            "\n\n Sample Number: Detected sample number"
            "\n Sample Value: Detected sample value"
            "\n\n Formula: data[i] & number, data[i] | number")
        
        msg.setWindowTitle("Programmer Analysis")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
               
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.setWindowTitle("Log Inceleme Arayuzu V5.5")
    window.resize(300, 300)
    window.show()
    sys.exit(app.exec())
