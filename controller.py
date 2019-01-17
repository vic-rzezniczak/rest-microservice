import ctypes
import hashlib
import requests as r

import data



def connect():
    comm_lib = ctypes.windll.LoadLibrary("plcommpro.dll") ### connecting to a library
    conn_params = ctypes.create_string_buffer(data._DEV_ADDR) ### connection parametres
    dev_handle = comm_lib.Connect(conn_params) ### connecting with device
    info_buffer = ctypes.create_string_buffer(2048)
    info_items = ctypes.create_string_buffer(b"DeviceID, Door1SensorType, Door1Drivertime, Door1Intertime") ### getting device information
    dev_info = comm_lib.GetDeviceParam(dev_handle, info_buffer, 256, info_items) ### test of connection
    '''opening doors'''
    comm_lib.ControlDevice(dev_handle, 1, 1, 2, 6, 0, '') #oper_id, door_num, door_output_oper, oper, none, none
    return comm_lib, dev_handle

def get_event(dll_handle=None, dev_handle=None):
    '''listener of events'''
    data._LOG = ctypes.create_string_buffer(256) ### creating an empty buffer
    dll_handle.GetRTLog(dev_handle, data._LOG, 256) ### passing a single log to a buffer
    line = data._LOG.value.decode() ### making bytes buffer a string so it's easier to parse
    time = line.split(',')[0] ### time of event
    card = line.split(',')[2] ### card no.
    return time, card

def hash_query(time='', card='', key=''):
    code = hashlib.md5() #making a hash code instance
    code.update(time.encode('utf-8'))
    code.update('wiktor-src'.encode('utf-8'))
    code.update('phpstorm'.encode('utf-8'))
    code.update(card.encode('utf-8'))
    code.update('undetermined'.encode('utf-8'))
    code.update(key.encode('utf-8'))
    return code

def perform_query(hash_code=''):
    data._POST['timeOf'] = data._TIME
    data._POST['plate'] = data._CARD
    data._POST['hash'] = hash_code.hexdigest()
    data._RESP = r.post(data._SERVER_ADDR, data._POST).json() ### destination address, post data
    
def contorl_device(request={}):
    try:
        if request['access'] == 'GRANTED':
            '''we open the door'''
            data._COMM_LIB.ControlDevice(data._DEV, 1, 1, 2, 6, 0, '') ### oper_id, door_num, door_output_oper, oper, none, none
        elif request['acces'] != 'GRANTED': pass
    except KeyError: pass
    
