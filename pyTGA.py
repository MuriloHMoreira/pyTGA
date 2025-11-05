import csv
import minimalmodbus
import serial
import signal
import sys
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ctypes
import numpy as np
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok

name = 'Ensaio_teste10CACsemfibra1'


##################################################
##################################################
##################################################
# Nao esquecer de salvar
##################################################
##################################################
##################################################
# Nao precisa editar nada abaixo
##################################################
##################################################
##################################################


def signal_handler(signal, frame):
    '''
    Function to close everything before stopping the test.
    '''
    f.close()
    print('Exiting Test!')
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)

def run_test_T(name, total_time, t_sleep, ctrl_ins, PLOT=True, LOGGING=True):
    '''
    Function to run a test. It will start the data aquisition module which 
    will run for a 'total_time' seconds. 
    Parameters
    ----------
    name : string
    The name of the test will be the name of the .csv file with the data of 
    the test.

    total_time: int, float
    The total time that the data aquisition module will run.
    
    t_sleep: int, float
    The time interveal between readings.
    
    scale_ser: serial.Serial
    The serial object of the scale.
    
    ctrl_ins: minimalmodbus.Instrument
    The instrument object of the controler.
    
    PLOT: bool
    The flag for plotting.
    
    LOGGING: bool
    The flag for logging the readings. Useful for debugging.

    Returns
    -------
    The numpy arrays with the time
    '''
    def signal_handler(signal, frame):
        '''
        Function to close everything before stopping the test.
        '''
        f.close()
        print('Exiting Test!')
        sys.exit()
    
    signal.signal(signal.SIGINT, signal_handler)
    print(f'Running Test: {name}')
    print(f'Total Time: {total_time}')
    f = open('./' + name + '.csv', 'w')
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(['t_label', 't', 'T', 'SP'])
    
    TEMP_REGISTER = 1
    SP_REGISTER = 25
    if PLOT:
        fig, axs = plt.subplots(1, 1, figsize=(9, 6))
        plt.ion()
        axs = [axs]
        line1_T, = axs[0].plot(0, 0, '-o', c='navy', label='Thermocouple')
        line2_SP, = axs[0].plot(0, 0, '-^', c='coral', label='Set Point')

        axs[0].set_xlabel('Time [s]')
        axs[0].set_ylabel('Temperature [°C]')
        for ax in axs:
            ax.grid()
        plt.subplots_adjust(wspace=0.3)
        plt.show()

    T1_reads = []
    SP_reads = []
    t_labels = []
    ts = []
    t_0 = time.time()
    t_end = time.time() + total_time
    while time.time() < t_end:
        try:
            t = time.time() - t_0
            t_label = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            T_data = ctrl_ins.read_register(TEMP_REGISTER)
            plt.pause(t_sleep / 2)
            SP_data = ctrl_ins.read_register(SP_REGISTER)
            T1_reads.append(T_data)
            SP_reads.append(SP_data)
            t_labels.append(t_label)
            ts.append(t)
            writer.writerow([t_label, t, T_data, SP_data])
            if LOGGING:
                print(f't={round(t, 2)}s | T = {T_data} °C | SP = {SP_data}°C')
        except:
            if LOGGING:
                print('Fail')
            else:
                pass
        if PLOT:
            line1_T.set_xdata(ts)
            line1_T.set_ydata(T1_reads)
            line2_SP.set_xdata(ts)
            line2_SP.set_ydata(SP_reads)
            fig.canvas.draw()
            for ax in axs:
                ax.relim()
                ax.autoscale_view()
        plt.pause(t_sleep / 2)
    f.close()
    print('That\'s all folks!')
    return np.array(ts), np.array(T1_reads), np.array(SP_reads)

PORT='COM1'
#Set up ctrl_ins
ctrl_ins = minimalmodbus.Instrument(PORT, 1, mode=minimalmodbus.MODE_RTU)
# ctrl_ins = minimalmodbus.Instrument(PORT, 1, mode=minimalmodbus.MODE_ASCII)

#Make the settings explicit
ctrl_ins.serial.baudrate = 9600
ctrl_ins.serial.bytesize = 8
ctrl_ins.serial.parity   = minimalmodbus.serial.PARITY_NONE
ctrl_ins.serial.stopbits = 1
ctrl_ins.precalculate_read_size = False
# ctrl_ins.debug = True
ctrl_ins.serial.timeout = 1
# Good practice
ctrl_ins.close_port_after_each_call = True
ctrl_ins.clear_buffers_before_each_transaction = True
minimalmodbus.MINIMALMODBUS_DEBUG = True
# minimalmodbus.serial.interCharTimeout = 1

def safe_read(instrument, register_address, n_trials=5, functioncode=3, DEBUG=False, PRINT_ONLY=False):
    READ = False
    i = 0
    register_value = None
    while not READ:
        if i > n_trials:
            READ = True
        try:
            if DEBUG:
                print(f'Trial: {i+1}')
            register_value = instrument.read_register(register_address, functioncode=functioncode)
            if PRINT_ONLY:
                print(register_value)
            READ = True
        except:
            if DEBUG:
                print('Failed!')
            time.sleep(0.5)
        i += 1
    if not PRINT_ONLY:
        return register_value

def safe_write(instrument, register_address, register_value, n_trials=5, functioncode=6, DEBUG=False):
    WROTE = False
    i = 0
    if DEBUG:
        print('Valor Atual: ', safe_read(instrument, register_address, n_trials=n_trials, DEBUG=DEBUG))

    while not WROTE:
        if i > 5:
            WROTE = True
        try:
            if DEBUG:
                print(f'Trial: {i+1}')
            instrument.write_register(register_address, register_value, functioncode=functioncode)
            WROTE = True
            print('Valor Registrado:', safe_read(instrument, register_address))
        except:
            if DEBUG:
                print('Failed!')
            time.sleep(0.5)
        i += 1
# X-1. Load heat-up curve
# 1
# 30 0
# 800 39
# 800 40
# 30 2

SP_0 = 30
SP_1 = 800
Pt_1 = 39
SP_2 = 800
Pt_2 = 40
SP_3 = 30
Pt_3 = 2

# X. Input loaded program to controller's program 1

# X.1. Set program to 1
time.sleep(0.5)

R_Prog_View = 72
R_Prog_Set = 73

# print('Programa Sendo Visualizado:')
# safe_write(ctrl_ins, R_Prog_View, 1, DEBUG=True)
# print('Programa Sendo Executado:')
# safe_write(ctrl_ins, R_Prog_Set, 1, DEBUG=True)

# print('Novo Programa Sendo Visualizado: ', safe_read(ctrl_ins, R_Prog_View))
# print('Novo Programa Sendo Executado: ',  safe_read(ctrl_ins, R_Prog_Set))

# X.2. Set time of first step 
time.sleep(0.5)

R_Pt_1 = 124
R_Pt_2 = 125
R_Pt_3 = 126
R_Pt_4 = 127
R_Pt_5 = 128
R_Pt_6 = 129
R_Pt_7 = 130

R_SP_0 = 131
R_SP_1 = 132
R_SP_2 = 133
R_SP_3 = 134
R_SP_4 = 135
R_SP_5 = 136
R_SP_6 = 137
R_SP_7 = 138

# print('Atual SP_0: ', safe_read(ctrl_ins, R_SP_0))
# print('Atual SP_1: ', safe_read(ctrl_ins, R_SP_1))
# print('Atual Pt_1: ', safe_read(ctrl_ins, R_Pt_1))
# print('Atual SP_2: ', safe_read(ctrl_ins, R_SP_2))
# print('Atual Pt_2: ', safe_read(ctrl_ins, R_Pt_2))
# print('Atual SP_3: ', safe_read(ctrl_ins, R_SP_3))
# print('Atual Pt_3: ', safe_read(ctrl_ins, R_Pt_3))

# safe_write(ctrl_ins, R_SP_0, SP_0)
# safe_write(ctrl_ins, R_SP_1, SP_1)
# safe_write(ctrl_ins, R_Pt_1, Pt_1)
# safe_write(ctrl_ins, R_SP_2, SP_2)
# safe_write(ctrl_ins, R_Pt_2, Pt_2)
# safe_write(ctrl_ins, R_SP_3, SP_3)
# safe_write(ctrl_ins, R_Pt_3, Pt_3)

# Run Program
R_Start = 47
safe_write(ctrl_ins, R_Start, 1)

R_SP_i = 0
R_PV_i = 1


# Set up Scale Reader
scale_ser = serial.Serial(port="COM2",
                          baudrate=4800,
                          timeout=None,
                          parity=serial.PARITY_EVEN,
                          stopbits=serial.STOPBITS_ONE,
                          bytesize=serial.SEVENBITS)


# Set up other TC Reader
# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# open unit
status["open_unit"] = tc08.usb_tc08_open_unit()
assert_pico2000_ok(status["open_unit"])
chandle = status["open_unit"]

# set mains rejection to 50 Hz
status["set_mains"] = tc08.usb_tc08_set_mains(chandle,0)
assert_pico2000_ok(status["set_mains"])

# set up channel
# therocouples types and int8 equivalent
# B=66 , E=69 , J=74 , K=75 , N=78 , R=82 , S=83 , T=84 , ' '=32 , X=88 
typeK = ctypes.c_int8(75)
status["set_channel"] = tc08.usb_tc08_set_channel(chandle, 1, typeK)
assert_pico2000_ok(status["set_channel"])

typeK = ctypes.c_int8(75)
status["set_channel"] = tc08.usb_tc08_set_channel(chandle, 2, typeK)
assert_pico2000_ok(status["set_channel"])

# get minimum sampling interval in ms
status["get_minimum_interval_ms"] = tc08.usb_tc08_get_minimum_interval_ms(chandle)
assert_pico2000_ok(status["get_minimum_interval_ms"])

# get single temperature reading
temp = (ctypes.c_float * 9)()
overflow = ctypes.c_int16(0)
units = tc08.USBTC08_UNITS["USBTC08_UNITS_CENTIGRADE"]

t_total = (Pt_1 + Pt_2 + Pt_3) * 60
print(f'Tempo total do ensaio: {t_total} s')

# Print the values


f = open('./Vitória de Alencar/' + name + '.csv', 'w')
writer = csv.writer(f, delimiter='\t')
writer.writerow(['t [s]', 'm [g]', 'Temp. Contr. [°C]', 'Temp. Prog. [°C]', 'Temp. Forno [°C]', 'Temp. Amos. [°C]'])


PV_reads = []
SP_reads = []
F_reads = []
S_reads = []
t_labels = []
ts = []


t = 0
while t < t_total:
    try:
        t_0 = time.time()

        SP_i = safe_read(ctrl_ins, R_SP_i)
        PV_i = safe_read(ctrl_ins, R_PV_i)
        bytesToRead = scale_ser.inWaiting()
        scale_data = scale_ser.read(bytesToRead)
        m = float(scale_data.decode("utf-8").split()[1])
        status["get_single"] = tc08.usb_tc08_get_single(chandle,ctypes.byref(temp), ctypes.byref(overflow), units)
        assert_pico2000_ok(status["get_single"])
        TC_F = round(temp[1], 2)
        TC_S = round(temp[2], 2)
        print(f'|  t: {round(t, 2)} s  |  m: {m} g  |  SP: {SP_i} C  |  PV: {PV_i} C  |  TC_F: {TC_F} C  |  TC_S: {TC_S} C  |')
        
        writer.writerow([t, m, PV_i, SP_i, TC_F, TC_S])
        f.flush()
        time.sleep(1)
        dt = time.time() - t_0
        t += dt
    except:
        pass
