import sys
import logging
import logging.config
import numpy as np
import pyqtgraph as pg
from time import sleep
from datetime import datetime as dt
from pyvisa import ResourceManager, errors
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QLineEdit, QLabel
from GUI.keithley_ui import Ui_MainWindow
from GUI.about_ui import Ui_Dialog

logging.config.fileConfig('src/Keithley_log.ini')
logger = logging.getLogger('root')

class Worker_IV(QThread):
    _data = pg.QtCore.Signal(object)
    _signal = pg.QtCore.Signal(int)
    _msg = pg.QtCore.Signal(str)
    
    def __init__(self, inst, infos, app):
        super(Worker_IV, self).__init__()
        logger.info('Initiate IV Worker.')
        self.app = app
        self.infos = infos
        try:
            self.measure_range = np.arange(float(self.infos["Start"]), 
                                           float(self.infos["Stop"]) + float(self.infos["Step"]), 
                                           float(self.infos["Step"]))
        except ValueError as ve:
            msg = f'Empty fields found. {ve}'
            logger.warning(msg)
            self._msg.emit(msg)
        self.inst  = inst
        self.x_vals = []
        self.y_vals = []
        self.std_vals = []
        self.is_running = True

    def stop(self):
        logger.info('Stopping Thread.')
        self.is_running = False
        self.terminate()

    def run(self):
        logger.info('Begining Measure.')
        self.app.save_btn.setEnabled(True)
        self.inst.write(f':SOUR:DEL {int(self.infos["Delay"])}')
        self.inst.write(f':SENS:CURR:PROT {float(self.infos["Compliance"])}')
        self.inst.write(f':SENS:FUNC "{self.infos["Source"]}", "{self.infos["Sensor"]}"')
        self.inst.write(':OUTP ON')
        try:
            for num, value in enumerate(self.measure_range):
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
                    self._data.emit((self.x_vals, self.y_vals, self.std_vals))
                    self._signal.emit(num)
                    sleep(0.2)
                except ValueError:
                    continue
                except errors.VisaIOError:
                    msg = 'Device not connected.'
                    self._msg.emit(msg)
                    logger.warning(msg)
        except AttributeError as ae:
            logger.warning(ae)
        self.inst.write(':OUTP OFF')
        self.app.save_btn.setEnabled(False)
        logger.info('Ending Measure.')

class Worker_Ohms(QThread):
    _data = pg.QtCore.Signal(object)
    _msg = pg.QtCore.Signal(str)
    
    def __init__(self, inst, infos, app):
        super(Worker_Ohms, self).__init__()
        logger.info('Initiate OHMS Worker.')
        self.infos = infos
        self.inst  = inst
        self.app = app
        self.x_vals = []
        self.y_vals = []
        self.std_vals = []
        self.is_running = True

    def stop(self):
        logger.info('Stopping Thread.')
        self.is_running = False
        self.terminate()

    def run(self):
        logger.info('Begining Measure.')
        self.app.save_btn.setEnabled(True)
        self.inst.write(f':SOUR:DEL {int(self.infos["Delay"])}')
        self.inst.write(f':SENS:FUNC "{self.infos["Sensor"].upper()}"')
        self.inst.write(f':SENS:{self.infos["Sensor"].upper()}:MODE MAN') 
        self.inst.write(f':SOUR:FUNC {self.infos["Source"].upper()}')
        self.inst.write(f':SOUR:{self.infos["Source"].upper()}:MODE FIX')
        self.inst.write(f':SOUR:{self.infos["Source"].upper()}:LEV {float(self.infos["Fixed Voltage"])}')
        self.inst.write(':OUTP ON')
        try:
            ri = 1
            while True:
                if self.app.thread_name['ohms'] is True:
                    for r1 in range(int(self.infos["Number of Measures"])):
                        _y = list()
                        try:
                            for r2 in np.arange(self.infos["Repetitions"]):
                                query = self.inst.query(':READ?').split(',')
                                _y.append(float(query[1]))
                                sleep(0.1)
                            self.x_vals.append(ri)
                            self.y_vals.append(float(np.mean(_y)))
                            self.std_vals.append(float(np.std(_y)))
                            self._data.emit((self.x_vals, self.y_vals, self.std_vals))
                            ri += 1
                        except ValueError:
                            continue
                        except errors.VisaIOError:
                            msg = 'Device not connected.'
                            self._msg.emit(msg)
                            logger.warning(msg)
                    self.app.thread_name['ohms'] = None
                    self.app._signal.emit('ohms')
                else:
                    if self.app.thread_name['ohms'] == False:
                        break
                    sleep(1)
        except AttributeError as ae:
            logger.warning(ae)
        self.inst.write(':OUTP OFF')
        self.app.save_btn.setEnabled(False)
        logger.info('Ending Measure.')

class Keithley_MainWindow(QMainWindow, Ui_MainWindow):
    _signal = pg.QtCore.Signal(str)

    def __init__(self, parent=None):
        super(Keithley_MainWindow, self).__init__(parent)
        logger.info('Starting App.')
        self.setupUi(self)
        self.setWindowIcon(QIcon('src/python_icon.ico'))
        self.setFixedSize(975, 570)
        self.rm = ResourceManager('@py')
        self.inst = self.connect_instrument()
        self.reset_instrument()
        self.thread_name = {}
        if self.get_id() == 'Device not connected.':
            self.message_box('Device not connected.')
        self.date_label.setText(f'Data: {dt.now().strftime("%d-%m-%Y")}')
        self.pwr_on_btn.clicked.connect(self.power_on)
        self.pwr_off_btn.clicked.connect(self.power_off)
        self.run_btn.clicked.connect(self.run_measure)
        self.save_btn.clicked.connect(self.auxiliar_func)
        self.save_btn.setEnabled(False)
        self.conn_btn.clicked.connect(self.connection)

        self.w2_rbtn.toggled.connect(self.select_wire_mode)
        self.w4_rbtn.toggled.connect(self.select_wire_mode)
        self.front_rbtn.toggled.connect(self.select_panel)
        self.rear_rbtn.toggled.connect(self.select_panel)

        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionExit.triggered.connect(self.close)
        self.actionSobre.triggered.connect(self.about_page)

        self.progressBar.setValue(0)
        self._signal.connect(self.show_dialog)
        self.measure_type.currentTextChanged.connect(self.value_changed)

        self.MplWidget.setBackground('w')
        self.MplWidget.setTitle("Medida", color="k", size="25pt")
        styles = {'color':'r', 'font-size':'25px'}
        self.MplWidget.setLabel('left', 'Current', units ='A', **styles)
        self.MplWidget.setLabel('bottom', 'Voltage', units ='V', **styles)
        self.graph = self.MplWidget.getPlotItem()

    def about_page(self):
        self.about_dialog = Ui_Dialog(self)
        self.about_dialog.show()

    def value_changed(self):
        styles = {'color':'r', 'font-size':'25px'}
        if self.measure_type.currentText() == 'IV':
            self.MplWidget.setLabel('left', 'Current', units ='A', **styles)
            self.MplWidget.setLabel('bottom', 'Voltage', units ='V', **styles)
            self.step_label.setText("Step")
            self.stop_label.setText("Stop")
            self.start_input = QLineEdit(self.gridLayoutWidget)
            self.start_input.setObjectName("start_input")
            self.range_grid.addWidget(self.start_input, 1, 1, 1, 1)
            self.start_label = QLabel(self.gridLayoutWidget)
            self.start_label.setObjectName("start_label")
            self.start_label.setText("Start")
            self.range_grid.addWidget(self.start_label, 1, 0, 1, 1)

        if self.measure_type.currentText() == 'Fixed Voltage':
            self.MplWidget.setLabel('left', 'Resistance', **styles)
            self.MplWidget.setLabel('bottom', 'Counts', **styles)
            self.step_label.setText("Measures")
            self.stop_label.setText("Voltage")
            self.start_input.deleteLater()
            self.start_label.deleteLater()

    def run_measure(self):
        if self.measure_type.currentText() == 'IV':
            self.range_size = ((float(self.stop_input.text()) - float(self.start_input.text())) \
                                / float(self.step_input.text()))
            self.progressBar.setMaximum(int(self.range_size))
            self.worker = Worker_IV(self.inst, self.get_info(), self)
            self.worker._signal.connect(self.signal_accept)
        if self.measure_type.currentText() == 'Fixed Voltage':
            self.thread_name['ohms'] = True
            self.worker = Worker_Ohms(self.inst, self.get_info(), self)
        self.worker._data.connect(self.update_plot_data)
        self.worker._msg.connect(self.message_box)
        self.worker.start()
    
    def signal_accept(self, msg):
        self.progressBar.setValue(int(msg))
    
    def message_box(self, msg):
        mbox = QMessageBox.about(self, "Warning", msg)
    
    def show_dialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Do you want to exchange sample?")
        end_btn = msg.addButton('End', msg.NoRole)
        continue_btn = msg.addButton('Continue', msg.YesRole)
        msg.setDefaultButton(continue_btn)
        msg.setEscapeButton(end_btn)
        response = msg.exec_()
        if response == 1:
            self.thread_name['ohms'] = True
        elif response == 0:
            self.thread_name['ohms'] = False

    def auxiliar_func(self):
        self.save_btn.setEnabled(False)
        logger.info('Aborting Measure.')
        self.worker.stop()

    def update_plot_data(self, values):
        self.x_vals = values[0]
        self.y_vals = values[1]
        self.std_values = values[2]
        self.graph.clear()
        self.graph.plot(self.x_vals, self.y_vals, pen=pg.mkPen(color=(0, 0, 0), width=4), 
                        symbol='o', symbolSize=10, symbolBrush=('k'))

    def connect_instrument(self):
        """Function to instanciate the instrument."""
        for instrument in self.rm.list_resources():
            try:
                k2400 = self.init_inst(instrument)
                k2400.timeout = 5000
                if k2400.query('*IDN?')[:8] == 'KEITHLEY':
                    return k2400
            except AttributeError as f:
                logger.warning(f'Unknown error - {f}')
            except errors.VisaIOError as e:
                logger.warning(f'Not possible to connect the port - {k2400}.')

    def init_inst(self, port):
        try:
            return self.rm.open_resource(
                    port, baud_rate=9600,
                    write_termination='\r', read_termination='\r'
                )
        except Exception as e:
            logger.warning(f'Initialization error -> {e}')

    def reset_instrument(self):
        """Function to reset instrument commands."""
        return self.inst.write('*RST')

    def get_id(self):
        """Function to get the instrument ID."""
        try:
            return self.inst.query('*IDN?')[:36]
        except errors.VisaIOError as e:
            logger.warning(e)
            return 'Device not connected.'

    def connection(self):
        self.conn_label.setText(self.get_id())
        self.conn_label.setWordWrap(True)

    def get_info(self):
        try:
            return {
                'User': self.user_input.text(),
                'Sample': self.user_input_2.text(),
                'Date': self.date_label.text()[6:],
                'Measure setup': '',
                'Start': self.start_input.text(),
                'Step': self.step_input.text(),
                'Stop': self.stop_input.text(),
                'Source': self.src_comboBox.currentText(),
                'Sensor': self.sns_comboBox.currentText(),
                'Compliance': float(self.comp_input.text()),
                'Delay': int(self.delay_input.text()),
                'Repetitions': self.repet_spinBox.value(),
                'Header': 'Voltage, Current, STD'
            }
        except RuntimeError:
                return {
                'User': self.user_input.text(),
                'Sample': self.user_input_2.text(),
                'Date': self.date_label.text()[6:],
                'Measure setup': '',
                'Number of Measures': self.step_input.text(),
                'Fixed Voltage': self.stop_input.text(),
                'Source': self.src_comboBox.currentText(),
                'Sensor': self.sns_comboBox.currentText(),
                'Compliance': float(self.comp_input.text()),
                'Delay': int(self.delay_input.text()),
                'Repetitions': self.repet_spinBox.value(),
                'Header': 'Counts, Ohms, STD'
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
                    if key != "Header":
                        file.write(f'{key}: {val}\n')
                file.write(f'\n')
                file.write(f'{self.get_info()["Header"]}\n')
                for line in zip(self.x_vals, self.y_vals, self.std_values):
                    file.write(f'{line[0]}, {line[1]}, {line[2]}\n')
        except ValueError as VE:
            logger.warning(f'Empty Field. -> {VE}')
        except Exception as e:
            logger.warning(f'{e}')
            pass
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
