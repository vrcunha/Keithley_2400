import numpy as np
import pyvisa as visa
from pyvisa import errors

rm = visa.ResourceManager('@py')

def init_instrument(rm, port):
    return rm.open_resource(port, baud_rate=9600,
                            write_termination='\r', read_termination='\r')
def connect_instrument():
    for instrument in rm.list_resources():
        try:
            inst = init_instrument(rm, instrument)
            inst.timeout = 5000
        except visa.errors.VisaIOError:
            print('Error to connect with Keithley.')
    return inst

def get_id(inst):
    print(inst.query('*IDN?')[:36])

def measure(inst, start, stop, step):
    result = ['volts, amps']
    for x in np.arange(start, stop, step):
        inst.write(f':SOUR:VOLT {x}')
        try:
            query = inst.query(':READ?').split(',')
            result.append(f'{query[0]}, {query[1]}')
        except visa.errors.VisaIOError as e:
            print(e)
    return result

def save_data(result):
    filename = input('Enter the filename: ')
    with open(f'{filename}.csv', 'w') as file:
        for line in result:
            file.write(f'{line}\n')

def set_source_delay(inst, delay=0):
    inst.write(f':SOUR:DEL {delay}')

def setting_measure(inst, source='VOLT', sensor='CURR'):
    inst.write(f':SENS:FUNC "{source}", "{sensor}"')

def turn_on(inst):
    inst.write(':OUTP ON')

def turn_off(inst):
    inst.write(':OUTP OFF')

def wich_panel(inst):
    print(inst.query(':ROUT:TERM?'))

def select_front_panel(inst):
    inst.write(':ROUT:TERM FRONT')

def select_rear_panel(inst):
    inst.write(':ROUT:TERM REAR')

def set_compliance(inst, value=100e-3):
    inst.write(f':SENS:CURR:PROT {value}')

def reset_instrument(inst):
    inst.write('*RST')

def wire_mode(inst):
    print(inst.query(':SYST:RSEN?'))

def two_wire_mode(inst):
    inst.write(':SYST:RSEN OFF')

def four_wire_mode(inst):
    inst.write(':SYST:RSEN ON')

def run_resistance_measure():
    pass

def run_IV_measure(inst, start, stop, step, source='VOLT', sensor='CURR', compliance=100e-3, delay = 0):
    get_id(inst)
    reset_instrument(inst)
    setting_measure(inst, source, sensor)
    set_compliance(inst, compliance)
    set_source_delay(inst, delay=0)
    turn_on(inst)
    result = measure(inst, start, stop, step)
    turn_off(inst)
    save_data(result)
