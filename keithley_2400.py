"""Script de comunicação com Keithley 2400."""

"""
Fontes:
https://pyvisa.readthedocs.io/en/1.8/example.html
https://www.ednasia.com/build-an-instrument-control-library-for-python/
https://www.edn.com/how-to-automate-measurements-with-python/
https://forum.tek.com/viewtopic.php?t=142166&__cf_chl_jschl_tk__=259f222b825c6e3a54ec47fb569c16c1ad759d9c-1611255674-0-AXex9tTnNwexpNL6gJiOs2uw_scjX7oeSo2SDvLnV1a8fj6v77nGNZfATHLGjqE1ZWqZLmTb96v2FXlRpk-Q2V17D0d_L897DIUTDhhvXKDqk0doKCT7QsQFMZDPwLfFEQy9i__h9_4U4l5UQ7pzO0883lbZEIP7Ul1Qs073w-qh_a2z6-dhKghjxJIvLJ4EeahYbXHMZUaKPHUV0JE4GfEHPOSHs-vWlwNUcsQ24c_FWdlI2CemhgYc1cUW4zpPk4M4L3WUKIrXmqaKnfwg_mIOtUaiLLqCOEpvmhLlxhd5fJbS7Q3-eImqNL6HUQeRJL9YPXACn5UQryo7p6UbZAXfB1zM6poEfZRRCpmqyiL4F-N6zBjlCXx22j-UtJ9MUi_gve2CmOde5WHP11jQWOY
https://forums.ni.com/t5/Instrument-Control-GPIB-Serial/PyVISA-with-Keithley-2400-SCPI/td-p/3555294?profile.language=pt-br
https://forum.tek.com/viewtopic.php?t=138989
"""
from pyvisa.highlevel import ResourceManager
from pyvisa.resources.resource import Resource
import serial
import pyvisa as visa
from pyvisa import constants, errors
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
from time import sleep 

KEITHLEY = 'ASRL1::INSTR'
BAUD_RATE = 9600

rm = visa.ResourceManager()

def init_instrument(rm: ResourceManager) -> Resource:
    return rm.open_resource(KEITHLEY, baud_rate=BAUD_RATE, 
                            write_termination='\r', read_termination='\r')

def list_instruments(rm: ResourceManager) -> None:
    print(rm.list_resources())
    return None

def get_ID(inst: Resource) -> None:
    print(inst.query('*IDN?')[:36])
    return None

def set_meas_range(inst: Resource, mtype: str, 
                   start: int, step: int, stop: int) -> None:
    inst.write(f':SOUR:{mtype}:STAR {start}')
    inst.write(f':SOUR:{mtype}:STOP {stop}')
    inst.write(f':SOUR:{mtype}:STEP {step}')
    print('Meas Range setted')
    # return None

def get_output(inst: Resource):
    pass

def turn_on_off(inst: Resource):
    # if :
    inst.write(':OUTP ON')
    # else: 
    inst.write(':OUTP OFF')

def select_panel(inst: Resource):
    inst.write(':ROUT:TERM REAR')
    inst.write(':ROUT:TERM FRONT')

def select_mode(inst: Resource):
    inst.write(':SYST:RSEN ON')
    inst.write(':SYST:RSEN OFF')

def set_compliance(inst: Resource, value='100e-3'):
    inst.write(f':SENS:CURR:PROT {value}')

def reset_instrument(inst: Resource):
    inst.write('*RST')

def init_measure(inst: Resource):
    inst.write(':INIT')
    inst.write(':READ?')

inst = init_instrument(rm)
get_ID(inst)
# set_meas_range(inst, 'VOLT', 0, 1, 5)


# inst.write('*IDN?')
# print(inst.read())
# while True:
#     print(inst.read_bytes(2))

# try:

# except errors.VisaIOError:


# inst.write(':SOUR:VOLT 0')
# inst.write(':SOUR:DEL 0.1')
# inst.write(':TRIG:COUN: 10')
# inst.query(':SOUR:FUNC VOLT')
# inst.write(':SOUR:CURR:LEV 50')
# inst.write(':SOUR:VOLT:RANG 20')
# inst.write(':SOUR:VOLT:LEV 2.5')
# inst.write(':SOUR:SWE:SPAC LIN')
# inst.write(':SOUR:FUNC CURR'log.)
# inst.write(':SOUR:CURR:MODE FIX')
# inst.write(':SOUR:SWE:RANG BEST')
# inst.write(':SOUR:VOLT:MODE SWE')
# inst.write(':SOUR:VOLT:RANG 10e-3')
# inst.write(':SENS:VOLT:RANG:AUTO ON')
# inst.write(':SENS:CURR:RANG:AUTO ON')







# fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)
# with open('_tempfile.txt','w') as f:
#     pass
# def animate(i):
#     graph_data = open('_tempfile.txt','r').read()
#     lines = graph_data.split('\n')
#     xs = list()
#     ys = list()
#     for line in lines:
#         pdb.set_trace()
#         if len(line) > 1:
#             x,y = line.split(',')
#             xs.append(float(x))
#             ys.append(float(y))
#     ax1.clear()
#     ax1.plot(xs,ys)

# ani = animation.FuncAnimation(fig, animate, interval=1000)
# plt.show()