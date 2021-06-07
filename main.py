import matplotlib.pyplot as plt
import pyvisa as visa
from pyvisa import errors
from instrument.keithley_2400 import init_instrument, process

rm = visa.ResourceManager('@py')

for instrument in rm.list_resources():
    try:
        inst = init_instrument(rm, instrument)
        inst.timeout = 5000
    except visa.errors.VisaIOError:
        print('Erro ao conectar com  O Keithley.')

settings_dict = {
    'start': -0.5,
    'stop': 3,
    'step': 0.5,
    'source':'VOLT',
    'sensor':'CURR',
    'compliance':'100e-3',
    'delay': 0
}

process(inst, **settings_dict)
