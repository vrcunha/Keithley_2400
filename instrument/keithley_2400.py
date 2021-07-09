import numpy as np
from time import sleep
import matplotlib.pyplot as plt
from pyvisa import ResourceManager, errors

class Keithley(object):
    """docstring for Keithley."""
    def __init__(self):
        super(Keithley, self).__init__()
        self.rm = ResourceManager('@py')
        self.inst = self.connect_instrument()
        self.reset_instrument()
        self.x_vals = []
        self.y_vals = []
        self.std_vals = []
        fig = plt.figure()
        self.axes = fig.add_subplot(111)
        self.graph = self.axes.plot([], [])

    def init_inst(self, port):
        try:
            return self.rm.open_resource(
                    port, baud_rate=9600,
                    write_termination='\r', read_termination='\r'
                )
        except Exception as e:
            print(e)

    def connect_instrument(self):
        """Function to instanciate the instrument."""
        for instrument in self.rm.list_resources():
            try:
                inst = self.init_inst(instrument)
                inst.timeout = 5000
            except errors.VisaIOError as e:
                print(e)
        return inst

    def get_id(self):
        try:
            print(self.inst.query('*IDN?')[:36])
        except errors.VisaIOError as e:
            print(f'{e}')

    def setting_measure(self):
        """Function to set the source and the sense."""
        self.inst.write(':SYST:RSEN OFF')
        self.inst.write(f':ROUT:TERM FRONT')
        self.inst.write(f':SOUR:DEL {0}')
        self.inst.write(f':SENS:CURR:PROT {100e-3}')
        self.inst.write(f':SENS:FUNC "VOLT", "CURR"')
        start = 0
        stop = 2.5
        step = 0.1
        self.measure_range = np.arange(start, stop+step, step)

    def measure(self):
        for value in self.measure_range:
            # if self.abort_measure:
            #     break
            self.inst.write(f':SOUR:VOLT {value}')
            print(value)
            _x = list()
            _y = list()
            for _repetition in np.arange(1):
                try:
                    query = self.inst.query(':READ?').split(',')
                except errors.VisaIOError as e:
                    print('Not possible to read the device.')
                _x.append(float(query[0]))
                _y.append(float(query[1]))
                sleep(0.1)
            self.x_vals.append(float(np.mean(_x)))
            self.y_vals.append(float(np.mean(_y)))
            self.std_vals.append(float(np.std(_y)))
            print(np.mean(_x), np.mean(_y))
            self.update_plot_data()

        # def abort_func(self):
        #     print(self.abort_measure)
        #     if not self.abort_measure:
        #         self.abort_measure = True
        #     else:
        #         self.abort_measure = False
        #     print(self.abort_measure)

    def run_IV_measure(self):
        """Function that run measure."""
        self.setting_measure()
        self.power_on()
        self.measure()
        self.power_off()

    def update_plot_data(self):
        self.graph.clear()
        self.graph.setData(self.x_vals, self.y_vals)
        self.graph.draw()
        # self.result = self.result + 1
        # print(self.result)
        # # self.data_line.clear()
        # print(self.x_vals)
        # self.graph.plot(self.x_vals, self.y_vals)
        # self.figure.canvas.draw()
        # self.data_line.setData(self.x_vals, self.y_vals)

    def reset_instrument(self):
        """Function to reset instrument commands."""
        return self.inst.write('*RST')

    def get_id(self):
        """Function to get the instrument ID."""
        try:
            return self.inst.query('*IDN?')[:36]
        except errors.VisaIOError as e:
            print(e)
            return 'Device not connected.'

    def connection(self):
        self.conn_label.setText(self.get_id())
        self.conn_label.setWordWrap(True)

    def get_info(self):
        return {
            'User': self.user_input.text(),
            'Date': self.date_label.text()[6:],
            'Measure range': '',
            'Start': float(self.start_input.text()),
            'Step': float(self.step_input.text()),
            'Stop': float(self.stop_input.text()),
            'Measure setup': '',
            'Source': self.src_comboBox.currentText(),
            'Sensor': self.sns_comboBox.currentText(),
            'Compliance': float(self.set_compliance()),
            'Delay': int(self.delay_input.text()),
            'Repetitions': self.repet_spinBox.value()
        }

    def power_on(self):
        """Function to turn keithley on."""
        return self.inst.write(':OUTP ON')

    def power_off(self):
        """Function to turn keithley off."""
        return self.inst.write(':OUTP OFF')

    # def select_panel(self):
    #     """Function to select panel."""
    #     radio_btn = self.sender()
    #     if radio_btn.isChecked():
    #         term = radio_btn.text()[:-9]
    #         print(term)
    #         return self.inst.write(f':ROUT:TERM {term.upper()}')
    #
    # def select_wire_mode(self):
    #     radio_btn = self.sender()
    #     if radio_btn.isChecked():
    #         n_wire = int(radio_btn.text()[0])
    #         if n_wire == 2:
    #             return self.inst.write(':SYST:RSEN OFF')
    #         elif n_wire == 4:
    #             return self.inst.write(':SYST:RSEN ON')


k = Keithley()
# inst = k.connect_instrument()
# k.get_id()
k.run_IV_measure()
