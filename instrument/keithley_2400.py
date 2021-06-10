import logging
import logging.config
import numpy as np
import pyvisa as visa
from pyvisa import errors

logging.config.fileConfig('Keithley_log.ini')
logger = logging.getLogger('root')

rm = visa.ResourceManager('@py')

def init_instrument(rm, port):
    """Function to configure and open the resource."""
    try:
        return rm.open_resource(port, baud_rate=9600,
                                write_termination='\r', read_termination='\r')
    except Exception as e:
        logger.warning(e)

def connect_instrument():
    """Function to instanciate the instrument."""
    for instrument in rm.list_resources():
        try:
            inst = init_instrument(rm, instrument)
            inst.timeout = 5000
        except visa.errors.VisaIOError as e:
            logger.warning(e)
    return inst

def get_id(inst):
    """Function to get the instrument ID."""
    return inst.query('*IDN?')[:36]

def measure(inst, start, stop, step):
    """Function that configures the measure."""
    result = ['volts, amps']
    for x in np.arange(start, stop, step):
        inst.write(f':SOUR:VOLT {x}')
        try:
            query = inst.query(':READ?').split(',')
            result.append(f'{query[0]}, {query[1]}')
        except visa.errors.VisaIOError as e:
            logger.warning(e)
    return result

def save_data(result, name):
    """Function to save the measure in file."""
    try:
        with open('.'.join(name), 'w') as file:
            for line in result:
                file.write(f'{line}\n')
    except Exception as e:
        logger.warning(f'{e}')
    return None

def set_source_delay(inst, delay=0):
    """Function to set the delay."""
    return inst.write(f':SOUR:DEL {delay}')

def setting_measure(inst, source='VOLT', sensor='CURR'):
    """Function to set the source and the sense."""
    return inst.write(f':SENS:FUNC "{source}", "{sensor}"')

def turn_on(inst):
    """Function to turn keithley on."""
    return inst.write(':OUTP ON')

def turn_off(inst):
    """Function to turn keithley off."""
    return inst.write(':OUTP OFF')

def set_compliance(inst, value=100e-3):
    """Function to set compliance."""
    return inst.write(f':SENS:CURR:PROT {value}')

def reset_instrument(inst):
    """Function to reset instrument commands."""
    return inst.write('*RST')

def select_panel(inst, panel='FRONT'):
    """Function to select panel."""
    response = inst.query(':ROUT:TERM?')
    if response == panel:
        return None
    elif response != panel:
        if panel == 'FRONT':
            return inst.write(':ROUT:TERM FRONT')
        else:
            return inst.write(':ROUT:TERM REAR')

def select_wire_mode(inst, mode='2Wire'):
    response = inst.query(':SYST:RSEN?')
    if response == '0' and mode=='2Wire':
        return None
    elif response == '1' and mode=='4Wire':
        return None
    elif response == '0' and mode=='4Wire':
        return inst.write(':SYST:RSEN ON')
    elif response == '1' and mode=='2Wire':
        return inst.write(':SYST:RSEN OFF')

def run_resistance_measure():
    pass

def run_IV_measure(inst, start, stop, step, source='VOLT', sensor='CURR', compliance=100e-3, delay = 0):
    """Function that run measure."""
    logger.debug('Início da Medida')
    reset_instrument(inst)
    select_panel(inst, panel='FRONT')
    two_wire_mode(inst)
    setting_measure(inst, source, sensor)
    set_compliance(inst, compliance)
    set_source_delay(inst, delay=0)
    turn_on(inst)
    result = measure(inst, start, stop, step)
    turn_off(inst)
    logger.debug('Fim da Medida')

if __name__ == 'main':
    inst = connect_instrument()
    print(get_id(inst))
