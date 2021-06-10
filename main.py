import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from instrument.keithley_2400 import connect_instrument, run_IV_measure
from GUI.keithley_ui import Ui_MainWindow

# TODO: implementar test
# TODO: botão abort medida
# TODO: função para medição de resistencia com tensao cte

settings_dict = {
    'start': -0.5,
    'stop': 3,
    'step': 0.5,
    'source':'VOLT',
    'sensor':'CURR',
    'compliance':100e-3,
    'delay': 0
}

class Keithley_MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Keithley_MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.pwr_on_btn.clicked.connect(self.power_on)
        self.pwr_off_btn.clicked.connect(self.power_off)
        self.conn_btn.clicked.connect(self.connection)
        self.run_btn.clicked.connect(self.run)
        self.save_btn.clicked.connect(self.save_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionSobre.triggered.connect(self.open_file)
        self.actionExit.triggered.connect(self.close)

    def power_on(self):
        pass

    def power_off(self):
        pass

    def connection(self):
        connect_instrument()

    def run(self):
        pass

    def save_file(self):
        from instrument.keithley_2400 import save_data
        name = QFileDialog.getSaveFileName(self, 'Save File',
                                           '', 'csv')
        # TODO: PEGAR O RESULTADO
        save_data(list([1,'2\n',3,4]), name)

    def open_file(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                        'All Files (*.*)')
        if path != ('', ''):
            print("File path : "+ path[0])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    UI = Keithley_MainWindow()
    UI.show()
    sys.exit(app.exec_())
