import sys
import logging
import logging.config
import numpy as np
import pyqtgraph as pg
from time import sleep
from datetime import datetime as dt
from pyvisa import ResourceManager, errors
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from GUI.keithley_ui import Ui_MainWindow

logging.config.fileConfig('Keithley_log.ini')
logger = logging.getLogger('root')

# TODO: Message Box
# TODO: função para medição de resistencia com tensao cte
# TODO: implementar test

class Worker(QThread):
    _data = pg.QtCore.Signal(object)
    
    def __init__(self, inst, infos):
        super(Worker, self).__init__()
        self.infos = infos
        try:
            self.measure_range = np.arange(float(self.infos["Start"]), 
                                           float(self.infos["Stop"]) + float(self.infos["Step"]), 
                                           float(self.infos["Step"]))
        except ValueError:
            print('Preencha todos os valores.')
        self.inst  = inst
        self.x_vals = []
        self.y_vals = []
        self.std_vals = []
        self.is_running = True

    def stop(self):
        self.is_running = False
        print('Stopping Thread.')
        self.terminate()

    def run(self):
        self.inst.write(f':SOUR:DEL {int(self.infos["Delay"])}')
        self.inst.write(f':SENS:CURR:PROT {float(self.infos["Compliance"])}')
        self.inst.write(f':SENS:FUNC "{self.infos["Source"]}", "{self.infos["Sensor"]}"')
        self.inst.write(':OUTP ON')
        try:
            for value in self.measure_range:
                try:
                    self.inst.write(f':SOUR:VOLT {value}')
                    _x = list()
                    _y = list()
                    for r in np.arange(self.infos["Repetitions"]):
                        query = self.inst.query(':READ?').split(',')
                        _x.append(float(query[0]))
                        _y.append(float(query[1]))
                        sleep(0.1)
                    self.x_vals.append(float(np.mean(_x)))
                    self.y_vals.append(float(np.mean(_y)))
                    self.std_vals.append(float(np.std(_y)))
                    self._data.emit((self.x_vals, self.y_vals))
                    sleep(0.2)
                except ValueError:
                    continue
        except AttributeError as ae:
            print(ae)
        self.inst.write(':OUTP OFF')

class Keithley_MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Keithley_MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.rm = ResourceManager('@py')
        self.inst = self.connect_instrument()
        self.reset_instrument()
        self.date_label.setText(f'Data: {dt.now().strftime("%d-%m-%Y")}')
        self.pwr_on_btn.clicked.connect(self.power_on)
        self.pwr_off_btn.clicked.connect(self.power_off)
        self.run_btn.clicked.connect(self.run_measure)
        self.save_btn.clicked.connect(self.abort_func)
        self.conn_btn.clicked.connect(self.connection)

        self.w2_rbtn.toggled.connect(self.select_wire_mode)
        self.w4_rbtn.toggled.connect(self.select_wire_mode)
        self.front_rbtn.toggled.connect(self.select_panel)
        self.rear_rbtn.toggled.connect(self.select_panel)

        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionExit.triggered.connect(self.close)

        self.MplWidget.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))
        self.graph = self.MplWidget.getPlotItem()

    def run_measure(self):
        self.worker = Worker(self.inst, self.get_info())
        self.worker._data.connect(self.update_plot_data)
        self.worker.start()

    def abort_func(self):
        print('Abortar medida')
        self.worker.stop()

    def update_plot_data(self, values):
        x_vals = values[0]
        y_vals = values[1]
        self.graph.plot(x_vals, y_vals)

    def connect_instrument(self):
        """Function to instanciate the instrument."""
        for instrument in self.rm.list_resources():
            try:
                k2400 = self.init_inst(instrument)
                k2400.timeout = 5000
            except AttributeError:
                print('Unknown error')
                # logger.warning(e)
            except errors.VisaIOError as e:
                print('Not possible to connect the device.')
                # logger.warning(e)
        return k2400

    def init_inst(self, port):
        try:
            return self.rm.open_resource(
                    port, baud_rate=9600,
                    write_termination='\r', read_termination='\r'
                )
        except Exception as e:
            print(f'Initialization error -> {e}')
            # logger.warning(e)

    def reset_instrument(self):
        """Function to reset instrument commands."""
        return self.inst.write('*RST')

    def get_id(self):
        """Function to get the instrument ID."""
        try:
            return self.inst.query('*IDN?')[:36]
        except errors.VisaIOError as e:
            # logger.warning(e)
            return 'Device not connected.'

    def connection(self):
        self.conn_label.setText(self.get_id())
        self.conn_label.setWordWrap(True)

    def get_info(self):
        return {
            'User': self.user_input.text(),
            'Date': self.date_label.text()[6:],
            'Measure range': '',
            'Start': self.start_input.text(),
            'Step': self.step_input.text(),
            'Stop': self.stop_input.text(),
            'Measure setup': '',
            'Source': self.src_comboBox.currentText(),
            'Sensor': self.sns_comboBox.currentText(),
            'Compliance': float(self.comp_input.text()),
            'Delay': int(self.delay_input.text()),
            'Repetitions': self.repet_spinBox.value()
        }

    def power_on(self):
        """Function to turn keithley on."""
        return self.inst.write(':OUTP ON')

    def power_off(self):
        """Function to turn keithley off."""
        return self.inst.write(':OUTP OFF')

    def select_panel(self):
        """Function to select panel."""
        radio_btn = self.sender()
        if radio_btn.isChecked():
            term = radio_btn.text()[:-9]
            print(term)
            return self.inst.write(f':ROUT:TERM {term.upper()}')

    def select_wire_mode(self):
        radio_btn = self.sender()
        if radio_btn.isChecked():
            n_wire = int(radio_btn.text()[0])
            if n_wire == 2:
                return self.inst.write(':SYST:RSEN OFF')
            elif n_wire == 4:
                return self.inst.write(':SYST:RSEN ON')

    def save_file(self):
        name = QFileDialog.getSaveFileName(self,
                                           'Save File',
                                           '',
                                           '.csv')
        try:
            with open(''.join(name), 'w') as file:
                for key, val in self.get_info().items():
                    file.write(f'{key}: {val}\n')
                file.write(f'\n')
                for line in self.result:
                    file.write(f'{line}\n')
        except ValueError as VE:
            print('Empty Field, fill all fields.')
            # logger.warning(f'{VE}')
        except Exception as e:
            pass
            # logger.warning(f'{e}')
        return None

    def open_file(self):
        path = QFileDialog.getOpenFileName(self,
                                           'Open a file',
                                            '',
                                            'All Files (*.*)')
        if path != ('', ''):
            print("File path : "+ path[0])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    UI = Keithley_MainWindow()
    UI.show()
    sys.exit(app.exec_())
