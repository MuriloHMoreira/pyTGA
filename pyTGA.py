import csv
import minimalmodbus
import serial
import signal
import sys
import os
import subprocess
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ctypes
import numpy as np
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok

for i in range(10):
    print('\n')
print('#' * 79)
print('#' * 79)
print('#' * 29, 'BEM-VINDO AO pyTGA!', '#' * 29)
print('#' * 79)
print('#' * 79)
print('\n')
print('#' * 33, 'INSTRUCOES:', '#' * 33)
print('#' * 5, '1. Insira o nome do arquivo:')
print('#' * 5, '2. Clique em Enter para começar o teste.')
print('#' * 5, '3. Para abortar o teste, clique Ctrl+C.')
print('\n')
print('#' * 33, 'IMPORTANTE:', '#' * 33)
print('#' * 15, 'Em caso de duvidas procure o Murilo ou o Tulio.', '#' * 15)
print('#' * 79)
print('\n')


name = input('##### Digite o nome do teste: ')
file_path = './Vitória de Alencar/' + name + '.csv'


resposta = 'SIM'
if os.path.isfile(file_path):
    print(f'##### OPA! O arquivo "{name}.csv" ja existe. Deseja sobrescrever?')
    resposta = input('##### Digite "SIM" para sobrescrever: ')

if resposta != 'SIM':
    sys.exit()

#os.system('python pyTGA_viewer.py')
subprocess.Popen(f'python pyTGA_viewer.py {name}')

run_flag = True

def signal_handler(signal, frame):
    '''
    Function to close everything before stopping the test.
    '''
    R_Start = 47
    time.sleep(1)
    safe_write(ctrl_ins, R_Start, 0, DEBUG=False, n_trials=15, SILENT=True)
    f.close()
    print('##### Ensaio Abortado! Dados salvos!')
    print('##### Por favor, verifique se o controlador parou.')
    global run_flag
    run_flag = False
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)

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

def safe_write(instrument, register_address, register_value, n_trials=5, functioncode=6, DEBUG=False, SILENT=False):
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
            if not SILENT:
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
safe_write(ctrl_ins, R_Start, 1, SILENT=True)

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
print(f'##### Tempo total do ensaio: {t_total} s')

# Print the values

f = open(file_path, 'w', newline='')
writer = csv.writer(f, delimiter=',')
writer.writerow(['t [s]', 'm [g]', 'Temp. Contr. [C]', 'Temp. Prog. [C]', 'Temp. Forno [C]', 'Temp. Amos. [C]'])


PV_reads = []
SP_reads = []
F_reads = []
S_reads = []
t_labels = []
ts = []


t = 0
print(f'##### Começou!')
print('\n')
while (t < t_total) and (run_flag):
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
