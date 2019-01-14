import ctypes
import hashlib
import requests as r

import data



def connect():
    comm_lib = ctypes.windll.LoadLibrary("plcommpro.dll") ### connecting to a library
    dev_str = ctypes.create_string_buffer(data._dev_addr) ### connection parametres
    dev_handle = comm_lib.Connect(dev_str) ### connecting with device
    info_buffer = ctypes.create_string_buffer(2048)
    info_items = ctypes.create_string_buffer(b"DeviceID, Door1SensorType, Door1Drivertime, Door1Intertime") ### getting device information
    dev_info = comm_lib.GetDeviceParam(dev_handle, info_buffer, 256, info_items) ### test of connection
    '''opening doors'''
    comm_lib.ControlDevice(dev_handle, 1, 1, 2, 6, 0, '') #oper_id, door_num, door_output_oper, oper, none, none
    return comm_lib, dev_handle

def get_event(dll_handle=None, dev_handle=None):
    '''listener of events'''
    rt_log = ctypes.create_string_buffer(256) ### creating an empty buffer
    dll_handle.GetRTLog(dev_handle, rt_log, 256) ### passing a single log to a buffer
    line = rt_log.value.decode() ### making bytes buffer a string so it's easier to parse
    time = line.split(',')[0] ### time of event
    card = line.split(',')[2] ### card no.
    return time, card

def hash_query():
    pass

def perform_query():
    pass
    
