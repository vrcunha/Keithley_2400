from instrument.keithley_2400 import connect_instrument, process

settings_dict = {
    'start': -0.5,
    'stop': 3,
    'step': 0.5,
    'source':'VOLT',
    'sensor':'CURR',
    'compliance':'100e-3',
    'delay': 0
}

if __name__ == '__main__':
    Keithley = connect_instrument()
    process(Keithley, **settings_dict)
