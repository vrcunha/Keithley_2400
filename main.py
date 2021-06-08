from instrument.keithley_2400 import connect_instrument, run_IV_measure

# TODO: colocar log no programa
# TODO: começar interface gráfica com pyqt
# TODO: fazer função para medição de resistencia com tensao cte

settings_dict = {
    'start': -0.5,
    'stop': 3,
    'step': 0.5,
    'source':'VOLT',
    'sensor':'CURR',
    'compliance':100e-3,
    'delay': 0
}

if __name__ == '__main__':
    Keithley = connect_instrument()
    run_IV_measure(Keithley, **settings_dict)
