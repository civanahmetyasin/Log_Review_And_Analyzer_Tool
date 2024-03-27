# read csv file
from PyQt6 import QtGui
from PyQt6.QtWidgets import QFileDialog,  QWidget, QApplication, QMessageBox, QLineEdit, QPushButton, QVBoxLayout, QScrollArea, QCheckBox, QTableWidget, QTableWidgetItem, QMenuBar, QInputDialog
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

        # read file path from yaml file
        if os.path.exists('CSV_reader_Config/file_path.yaml'):
            with open('CSV_reader_Config/file_path.yaml', 'r') as f:
                self.pathCSV = yaml.load(f, Loader=yaml.FullLoader)
                
        self.version = "1.7.0"

        self.setWindowTitle('CSV Reader V' + self.version)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setGeometry(300, 50, 400, 400)
        
        # add qmenu
        self.menuBar = QMenuBar()
        self.menuBar.setNativeMenuBar(False)
        self.fileMenu = self.menuBar.addMenu('File')
        self.fileMenu.setStyleSheet("""QMenu {background-color: #E1E1E1;
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
                            border-color: #777;}""")
        self.fileMenu.addAction('Open CSV File', self.read_csv)
        self.fileMenu.addAction('Exit', self.close)

        self.mathMenu = self.menuBar.addMenu('Math')
        self.mathMenu.setStyleSheet("""QMenu {background-color: #E1E1E1;
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
                            border-color: #777;}""")
        self.mathMenu.addAction('Math Calculation', self.mathCalculationWidget.show)
        self.mathMenu.addAction('Filters', self.filterWidget.show)

        self.configMenu = self.menuBar.addMenu('Config')
        self.configMenu.setStyleSheet("""QMenu {background-color: #E1E1E1;
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
                            border-color: #777;}""")
        self.configMenu.addAction('Set Separator', self.setSeparator)

        self.helpMenu = self.menuBar.addMenu('Help')
        self.helpMenu.setStyleSheet("""QMenu {background-color: #E1E1E1;
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
                            border-color: #777;}""")
        self.helpMenu.addAction('About', self.about)
        self.helpMenu.addAction('Help', self.help)
        self.helpMenu.addAction('Thanks', self.thanks)



        self.button = QPushButton('Open CSV file')
        self.button.clicked.connect(self.read_csv)
        self.button.setStyleSheet("""
                        QPushButton {
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
                        }
                    """)

        # add draw on the same graph checkbox
        self.drawOnTheSameGraphCheckBox = QCheckBox('Draw On the Same Graph')
        self.drawOnTheSameGraphCheckBox.setChecked(False)
        self.drawOnTheSameGraphCheckBox.setStyleSheet("""
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
            """)

        # add y axis twinx checkbox
        self.yAxisTwinxCheckBox = QCheckBox('Y Axis Twinx')
        self.yAxisTwinxCheckBox.setChecked(False)
        self.yAxisTwinxCheckBox.setStyleSheet("""
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
            """)

        # add separate line
        self.line2 = QWidget()
        self.line2.setFixedHeight(1)
        self.line2.setStyleSheet('background-color: black')

        self.fftCheckBox = QCheckBox('FFT on')
        self.fftCheckBox.setChecked(False)
        self.fftCheckBox.stateChanged.connect(self.fftCheckBoxChanged)
        self.fftCheckBox.setStyleSheet("""
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
            """)

        # add separate line
        self.line3 = QWidget()
        self.line3.setFixedHeight(1)
        self.line3.setStyleSheet('background-color: black')

        self.fftFrequency = QLineEdit()
        self.fftFrequency.setPlaceholderText('Sample Frequency')
        self.fftFrequency.setDisabled(True)
        self.fftFrequency.setStyleSheet("""
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
            """)

        self.openRawData = QCheckBox('Open Raw Data In Table')
        self.openRawData.setChecked(False)
        self.openRawData.setStyleSheet("""
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
            """)

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
        self.meanCheckBox.setStyleSheet("""
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
            """)

        self.searchField = QLineEdit()
        self.searchField.setPlaceholderText('Search')
        self.searchField.returnPressed.connect(self.search)
        self.searchField.textChanged.connect(self.search)
        self.searchField.setDisabled(True)
        self.searchField.setStyleSheet("""
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
            """)

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
        self.buttonStyle = """"""
        self.qButton = QPushButton()

        self.rawDataWidget = QWidget()

        # add math calculation widget
        self.mathCalculationWidget.setWindowTitle("Calculation")
        self.mathCalculationWidget.resize(250, 150)
        self.mathCalculationWidget.move(10, 30)
        self.mathCalculationWidget.show()

        self.filterWidget.setWindowTitle("Filter")
        self.filterWidget.resize(250, 150)
        self.filterWidget.move(10, 450)
        self.filterWidget.show()
        

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
        # add textbox for get number for math calculation
        self.mathCalculationTextBox = QLineEdit()
        self.mathCalculationTextBox.setPlaceholderText('Enter Number')
        self.mathCalculationTextBox.setStyleSheet(self.lineEditStyle)
        self.mathCalculationTextBox.setValidator(QtGui.QDoubleValidator())

        # add + - * / checkbox
        # checkbox style
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

        # clear buttons for new csv file not include read csv file button,

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

        else:
            # change window size
            self.resize(300, 300)
            self.searchField.setDisabled(True)
            QMessageBox.warning(self, 'Error', 'No file selected')

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
                self.table = QTableWidget()

                self.table.setColumnCount(1)
                self.table.setRowCount(len(data))

                # print to console as uint16_t c array without .0
                # print("uint16_t " + self.label_name + "[] = {")
                # for i in range(len(data)):
                #     if i == len(data)-1:
                #         print(str(int(data[i])))
                #     else:
                #         print(str(int(data[i])) + ",")
                # print("};")

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

                    # print to console as uint16_t c array without .0
                    # print("uint16_t " + self.label_name + "[] = {")
                    # for i in range(len(data)):
                    #     if i == len(data)-1:
                    #         print(str(int(data[i])))
                    #     else:
                    #         print(str(int(data[i])) + ",")
                    # print("};")

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

                    # print to console as uint16_t c array without .0
                    # print("uint16_t " + self.label_name + "[] = {")
                    # for i in range(len(data)):
                    #     if i == len(data)-1:
                    #         print(str(int(data[i])))
                    #     else:
                    #         print(str(int(data[i])) + ",")
                    # print("};")

                    # add data to table
                    for i in range(len(data)):
                        self.table.setItem(i, self.tableColumnCounter,
                                           QTableWidgetItem(str(data[i])))
                    # set column header name as line name
                    self.table.setHorizontalHeaderItem(
                        self.tableColumnCounter, QTableWidgetItem(self.label_name))

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
            self.fftFrequency.setStyleSheet("""
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
            """)

    def close_fig_event(self, event):
        counter = 0
        for title in self.titleList:
            if title == str(self.titleList[len(self.titleList)-1]):
                self.titleList.pop(counter)
                self.lineCounter = 0
            counter = counter + 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.setWindowTitle("Log Inceleme Arayuzu V4.1")
    window.resize(300, 300)
    window.show()
    sys.exit(app.exec())
