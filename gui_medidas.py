"""Docstring do módulo para satisfazer o linter."""
import sys
import matplotlib
matplotlib.use('Qt5Agg')

import PyQt5.QtCore as Core
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QColorDialog, QFontDialog, QMainWindow,
QMessageBox, QVBoxLayout, QTableWidget, QTableWidgetItem, QInputDialog, QFileDialog, QHBoxLayout)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class App(QMainWindow):
    """Docstring da classe app que é um teste."""
    def __init__(self):
        super(App, self).__init__()
        self.title = 'Janela de Teste - PyQt5'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        # self.setMinimumSize(QSize(640, 480))
        self.init_ui()

    def init_ui(self):
        """Docstring da função initUI."""
        

        # Initial Check
        # self.msg_box = QMessageBox.question(self.centralWidget, 'Open Box', 'Deseja iniciar o programa?',
        # QMessageBox.Yes | QMessageBox.No , QMessageBox.Yes)
        # if self.msg_box == QMessageBox.Yes:
        #     print('Ok.')
        # else:
        #     sys.exit()
        
        self.centralWidget = QWidget()
        self.statusBar().showMessage('Message in statusbar.')
        self.graph = MplCanvas(self.centralWidget, width=5, height=4, dpi=100)
        self.graph.axes.plot([0,1,2,3,4], [10,1,20,3,40])

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        self.toolbar = NavigationToolbar(self.graph, self.centralWidget)

        self.get_choice()
        self.tabela = QTableWidget()
        self.create_table()
        
        self.openFileNameDialog()
        self.openFileNamesDialog()
        self.saveFileDialog()

        # Widgets
        # Labels
        self.label = QLabel('PyQt5 simple window - Hello World!', self)
        self.label.move(int(self.width/2)+10, self.top)
        
        self.l1 = QLabel(self)
        self.l1.setText("On the Center")
        self.l1.setAlignment(Core.Qt.AlignCenter)

        self.l2 = QLabel(self)
        self.l2.setText("On the Left")
        self.l2.setAlignment(Core.Qt.AlignLeft)

        self.l4 = QLabel(self)
        self.l4.setText("On the Right")
        self.l4.setAlignment(Core.Qt.AlignRight)

        # Buttons
        self.btn1 = QPushButton('Botão', self)
        self.btn1.clicked.connect(self.print_func)
        self.btn1.move(int(self.width/2)+10, int(self.top)+30)
        self.btn2 = QPushButton('Botão Diag', self)
        # self.btn2.clicked.connect(self.showindow)
        self.btn2.move(int(self.width/2)+100, int(self.top)+30)
        # Inputs
        self.text_box = QLineEdit(self)
        self.text_box.move(int(self.width/2)+10, int(self.top)+60)
        self.text_box.resize(180, 20)
        
        self.button = QPushButton('Open color dialog', self)
        self.button.setToolTip('Opens color dialog')
        self.button.move(10,10)
        self.button.clicked.connect(self.open_color_dialog)

        self.button2 = QPushButton('Open PyQt5 Font Dialog', self)
        self.button2.setToolTip('font dialog')
        self.button2.move(50,50)
        self.button2.clicked.connect(self.openFontDialog)

        # Layout settings
        self.layout = QHBoxLayout()
        self.sub_layout1 = QVBoxLayout()
        self.sub_layout2 = QVBoxLayout()
        self.sub_layout3 = QVBoxLayout()
        self.layout.addLayout(self.sub_layout1)
        self.layout.addLayout(self.sub_layout3)
        self.layout.addLayout(self.sub_layout2)
        self.centralWidget.setLayout(self.layout)
        self.sub_layout1.addWidget(self.label)
        self.sub_layout1.addWidget(self.l1)
        self.sub_layout1.addWidget(self.l2)
        self.sub_layout1.addWidget(self.l4)
        self.sub_layout1.addWidget(self.btn1)
        self.sub_layout1.addWidget(self.btn2)
        self.sub_layout1.addWidget(self.text_box)
        self.sub_layout1.addWidget(self.button)
        self.sub_layout1.addWidget(self.button2)
        self.sub_layout3.addWidget(self.tabela)
        self.sub_layout2.addWidget(self.toolbar)
        self.sub_layout2.addWidget(self.graph)
        # Show method
        
        # Settings
        App.setCentralWidget(self, self.centralWidget)
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
    
        self.show()

    def openFontDialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            print(font.toString())

    def open_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            print(color.name())

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
    
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

    def create_table(self):
        """Docstring da função createTable."""
        self.tabela.setRowCount(4)
        self.tabela.setColumnCount(2)
        self.tabela.setItem(0,0, QTableWidgetItem("Cell (1,1)"))
        self.tabela.setItem(0,1, QTableWidgetItem("Cell (1,2)"))
        self.tabela.setItem(1,0, QTableWidgetItem("Cell (2,1)"))
        self.tabela.setItem(1,1, QTableWidgetItem("Cell (2,2)"))
        self.tabela.setItem(2,0, QTableWidgetItem("Cell (3,1)"))
        self.tabela.setItem(2,1, QTableWidgetItem("Cell (3,2)"))
        self.tabela.setItem(3,0, QTableWidgetItem("Cell (4,1)"))
        self.tabela.setItem(3,1, QTableWidgetItem("Cell (4,2)"))
        self.tabela.doubleClicked.connect(self.on_table)

    def on_table(self):
        """Some docstring for linter."""
        print("\n")
        for current_item in self.tabela.selectedItems():
            print(current_item.row(), current_item.column(), current_item.text())

    def print_func(self):
        """Docstring da função print_func."""
        print('O btn funfou.')

    def show_window(self):
        """Docstring da função showindow."""
        text_box_value = self.text_box.text()
        QMessageBox.question(self, 'Confirmation', "You typed: " + text_box_value,
                             QMessageBox.Ok, QMessageBox.Ok)
        self.text_box.setText("")

    def get_choice(self):
        items = ("Red","Blue","Green")
        item, ok = QInputDialog.getItem(self, "Get item","Color:", items, 0, False)
        if ok and item:
            print(item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()


# om PyQt5 import QtCore, QtGui, QtWidgets


# class Ui_MainWindow(object):
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(400, 300)
#         self.centralWidget = QtWidgets.QWidget(MainWindow)
#         self.centralWidget.setObjectName("centralWidget")
#         self.printbutton = QtWidgets.QPushButton(self.centralWidget)
#         self.printbutton.setGeometry(QtCore.QRect(20, 210, 75, 23))
#         self.printbutton.setObjectName("pushButton")
#         self.label = QtWidgets.QLabel(self.centralWidget)
#         self.label.setGeometry(QtCore.QRect(10, 30, 47, 13))
#         self.label.setObjectName("label")
#         self.textBrowser = QtWidgets.QTextBrowser(self.centralWidget)
#         self.textBrowser.setGeometry(QtCore.QRect(100, 10, 281, 51))
#         self.textBrowser.setObjectName("textBrowser")
#         self.lcdNumber = QtWidgets.QLCDNumber(self.centralWidget)
#         self.lcdNumber.setGeometry(QtCore.QRect(10, 100, 64, 23))
#         self.lcdNumber.setObjectName("lcdNumber")
#         self.countbutton = QtWidgets.QPushButton(self.centralWidget)
#         self.countbutton.setGeometry(QtCore.QRect(100, 210, 75, 23))
#         self.countbutton.setObjectName("pushButton_2")
#         self.textEdit = QtWidgets.QTextEdit(self.centralWidget)
#         self.textEdit.setGeometry(QtCore.QRect(100, 70, 104, 71))
#         self.textEdit.setObjectName("textEdit")
#         MainWindow.setCentralWidget(self.centralWidget)
#         self.menuBar = QtWidgets.QMenuBar(MainWindow)
#         self.menuBar.setGeometry(QtCore.QRect(0, 0, 400, 21))
#         self.menuBar.setObjectName("menuBar")
#         MainWindow.setMenuBar(self.menuBar)
#         self.mainToolBar = QtWidgets.QToolBar(MainWindow)
#         self.mainToolBar.setObjectName("mainToolBar")
#         MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
#         self.statusBar = QtWidgets.QStatusBar(MainWindow)
#         self.statusBar.setObjectName("statusBar")
#         MainWindow.setStatusBar(self.statusBar)

#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)

#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "ProgramaTeste"))
#         self.printbutton.setText(_translate("MainWindow", "Print"))
#         self.label.setText(_translate("MainWindow", "TextLabel"))
#         self.countbutton.setText(_translate("MainWindow", "Count"))

# from PyQt5 import QtCore, QtGui, QtWidgets

# class Ui_MainWindow(object):
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(553, 421)
#         self.centralWidget = QtWidgets.QWidget(MainWindow)
#         self.centralWidget.setObjectName("centralWidget")
#         self.printBut = QtWidgets.QPushButton(self.centralWidget)
#         self.printBut.setGeometry(QtCore.QRect(390, 100, 75, 23))
#         self.printBut.setObjectName("printBut")
#         self.label = QtWidgets.QLabel(self.centralWidget)
#         self.label.setGeometry(QtCore.QRect(10, 30, 47, 13))
#         self.label.setObjectName("label")
#         self.textBrowser = QtWidgets.QTextBrowser(self.centralWidget)
#         self.textBrowser.setGeometry(QtCore.QRect(90, 20, 281, 51))
#         self.textBrowser.setObjectName("textBrowser")
#         self.lcd = QtWidgets.QLCDNumber(self.centralWidget)
#         self.lcd.setGeometry(QtCore.QRect(390, 20, 131, 51))
#         self.lcd.setObjectName("lcd")
#         self.countBut = QtWidgets.QPushButton(self.centralWidget)
#         self.countBut.setGeometry(QtCore.QRect(470, 100, 75, 23))
#         self.countBut.setObjectName("countBut")
#         self.textEdit = QtWidgets.QTextEdit(self.centralWidget)
#         self.textEdit.setGeometry(QtCore.QRect(90, 100, 281, 31))
#         self.textEdit.setObjectName("textEdit")
#         self.radioBut = QtWidgets.QRadioButton(self.centralWidget)
#         self.radioBut.setGeometry(QtCore.QRect(10, 70, 82, 17))
#         self.radioBut.setObjectName("radioBut")
#         self.checkBox = QtWidgets.QCheckBox(self.centralWidget)
#         self.checkBox.setGeometry(QtCore.QRect(10, 90, 70, 17))
#         self.checkBox.setObjectName("checkBox")
#         self.graph = QtWidgets.QGraphicsView(self.centralWidget)
#         self.graph.setGeometry(QtCore.QRect(280, 160, 261, 191))
#         self.graph.setObjectName("graph")
#         self.tableView = QtWidgets.QTableView(self.centralWidget)
#         self.tableView.setGeometry(QtCore.QRect(10, 160, 256, 192))
#         self.tableView.setObjectName("tableView")
#         self.label_2 = QtWidgets.QLabel(self.centralWidget)
#         self.label_2.setGeometry(QtCore.QRect(100, 0, 81, 16))
#         self.label_2.setObjectName("label_2")
#         self.label_3 = QtWidgets.QLabel(self.centralWidget)
#         self.label_3.setGeometry(QtCore.QRect(100, 80, 81, 16))
#         self.label_3.setObjectName("label_3")
#         self.label_4 = QtWidgets.QLabel(self.centralWidget)
#         self.label_4.setGeometry(QtCore.QRect(20, 140, 81, 16))
#         self.label_4.setObjectName("label_4")
#         self.label_5 = QtWidgets.QLabel(self.centralWidget)
#         self.label_5.setGeometry(QtCore.QRect(290, 140, 81, 16))
#         self.label_5.setObjectName("label_5")
#         MainWindow.setCentralWidget(self.centralWidget)
#         self.menuBar = QtWidgets.QMenuBar(MainWindow)
#         self.menuBar.setGeometry(QtCore.QRect(0, 0, 553, 21))
#         self.menuBar.setObjectName("menuBar")
#         self.menu = QtWidgets.QMenu(self.menuBar)
#         self.menu.setObjectName("menu")
#         MainWindow.setMenuBar(self.menuBar)
#         self.statusBar = QtWidgets.QStatusBar(MainWindow)
#         self.statusBar.setObjectName("statusBar")
#         MainWindow.setStatusBar(self.statusBar)
#         self.Abrir = QtWidgets.QAction(MainWindow)
#         self.Abrir.setObjectName("Abrir")
#         self.Salvar = QtWidgets.QAction(MainWindow)
#         self.Salvar.setObjectName("Salvar")
#         self.Fechar = QtWidgets.QAction(MainWindow)
#         self.Fechar.setObjectName("Fechar")
#         self.menu.addAction(self.Abrir)
#         self.menu.addAction(self.Salvar)
#         self.menu.addAction(self.Fechar)
#         self.menuBar.addAction(self.menu.menuAction())

#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)
#         MainWindow.setTabOrder(self.graph, self.countBut)
#         MainWindow.setTabOrder(self.countBut, self.textEdit)
#         MainWindow.setTabOrder(self.textEdit, self.radioBut)
#         MainWindow.setTabOrder(self.radioBut, self.checkBox)
#         MainWindow.setTabOrder(self.checkBox, self.printBut)
#         MainWindow.setTabOrder(self.printBut, self.textBrowser)

#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
#         self.printBut.setText(_translate("MainWindow", "Print"))
#         self.label.setText(_translate("MainWindow", "TextLabel"))
#         self.countBut.setText(_translate("MainWindow", "Count"))
#         self.radioBut.setText(_translate("MainWindow", "RadioButton"))
#         self.checkBox.setText(_translate("MainWindow", "CheckBox"))
#         self.label_2.setText(_translate("MainWindow", "textBrowser"))
#         self.label_3.setText(_translate("MainWindow", "textEdit"))
#         self.label_4.setText(_translate("MainWindow", "Table"))
#         self.label_5.setText(_translate("MainWindow", "Graphic"))
#         self.menu.setTitle(_translate("MainWindow", "Arquivo"))
#         self.Abrir.setText(_translate("MainWindow", "Abrir"))
#         self.Salvar.setText(_translate("MainWindow", "Salvar"))
#         self.Fechar.setText(_translate("MainWindow", "Fechar"))

# import sys

# from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
# from PyQt5.QtGui import QIcon


# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
# import matplotlib.pyplot as plt

# import random

# class App(QMainWindow):

#     def __init__(self):
#         super().__init__()
#         self.left = 10
#         self.top = 10
#         self.title = 'PyQt5 matplotlib example - pythonspot.com'
#         self.width = 640
#         self.height = 400
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)

#         m = PlotCanvas(self, width=5, height=4)
#         m.move(0,0)

#         button = QPushButton('PyQt5 button', self)
#         button.setToolTip('This s an example button')
#         button.move(500,0)
#         button.resize(140,100)

#         self.show()


# class PlotCanvas(FigureCanvas):

#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)

#         FigureCanvas.__init__(self, fig)
#         self.setParent(parent)

#         FigureCanvas.setSizePolicy(self,
#                 QSizePolicy.Expanding,
#                 QSizePolicy.Expanding)
#         FigureCanvas.updateGeometry(self)
#         self.plot()


#     def plot(self):
#         data = [random.random() for i in range(25)]
#         ax = self.figure.add_subplot(111)
#         ax.plot(data, 'r-')
#         ax.set_title('PyQt Matplotlib Example')
#         self.draw()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = App()
#     sys.exit(app.exec_())


# class Dialog(QDialog):
#     NumGridRows = 3
#     NumButtons = 4

#     def __init__(self):
#         super(Dialog, self).__init__()
#         self.createFormGroupBox()
        
#         buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
#         buttonBox.accepted.connect(self.accept)
#         buttonBox.rejected.connect(self.reject)
        
#         mainLayout = QVBoxLayout()
#         mainLayout.addWidget(self.formGroupBox)
#         mainLayout.addWidget(buttonBox)
#         self.setLayout(mainLayout)
        
#         self.setWindowTitle("Form Layout - pythonspot.com")
        
#     def createFormGroupBox(self):
#         self.formGroupBox = QGroupBox("Form layout")
#         layout = QFormLayout()
#         layout.addRow(QLabel("Name:"), QLineEdit())
#         layout.addRow(QLabel("Country:"), QComboBox())
#         layout.addRow(QLabel("Age:"), QSpinBox())
#         self.formGroupBox.setLayout(layout)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     dialog = Dialog()
#     sys.exit(dialog.exec_())
