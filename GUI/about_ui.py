from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AboutWindow(object):
    def setupUi(self, AboutWindow):
        AboutWindow.setObjectName("AboutWindow")
        AboutWindow.resize(475, 228)
        self.centralwidget = QtWidgets.QWidget(AboutWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(9, 189, 451, 31))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.fechar_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.fechar_btn.setObjectName("fechar_btn")
        self.gridLayout.addWidget(self.fechar_btn, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 70, 191, 101))
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        AboutWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(AboutWindow)
        QtCore.QMetaObject.connectSlotsByName(AboutWindow)

    def retranslateUi(self, AboutWindow):
        _translate = QtCore.QCoreApplication.translate
        AboutWindow.setWindowTitle(_translate("AboutWindow", "Sobre"))
        self.fechar_btn.setText(_translate("AboutWindow", "Fechar"))
        self.label.setText(_translate("AboutWindow", "dsdfasdfsdfsfasdfasdfdfasdfasdfasdfasdfadfasdfafdasdfasdfasdfasdfasdfasdfadfas"))
