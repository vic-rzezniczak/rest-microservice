from io import BytesIO
from urllib.parse import urlencode
from imp import reload
import ctypes
import sys
import hashlib

import data



def connect():
    comm_lib = ctypes.windll.LoadLibrary("plcommpro.dll") ### connecting to a library
    dev_str = ctypes.create_string_buffer(data._addr) ### connection parametres
    dev_handle = comm_lib.Connect(dev_str) ### connecting with device
    info_buffer = ctypes.create_string_buffer(2048)
    info_items = ctypes.create_string_buffer(b"DeviceID, Door1SensorType, Door1Drivertime, Door1Intertime") ### getting device information
    dev_info = comm_lib.GetDeviceParam(dev_handle, info_buffer, 256, info_items)
    '''opening doors'''
    comm_lib.ControlDevice(dev_handle, 1, 1, 2, 6, 0, '') #oper_id, door_num, door_output_oper, oper, none, none
    return global comm_lib

input('\nShall I start?')


while 1:
    rt_log = ctypes.create_string_buffer(256) #creating a buffer, why I don't know
    comm_lib.GetRTLog(dev_handle, rt_log, 256) #passing a single log to a buffer
    log_line = rt_log.value.decode() #making bytes buffer a string so it's easier to parse
    #print(log_line)
    temp = log_line.split(',') #extracting needed data
    log_time = temp[0] #time of event
    log_card = temp[2] #card no.

    print('\nTIME: ', log_time, '\tCARD: ', log_card)

    
    ###if len(log_card) > 1: #we've got positive event
    ###print('\nTIME: ', log_time, '\tCARD: ', log_card)
    ###hashing
    code = hashlib.md5() #making a hash code instance
    code.update(log_time.encode('utf-8'))
    code.update('not-your-business'.encode('utf-8')) ### 'wiktor-src'
    code.update('phpstorm'.encode('utf-8'))
    code.update(log_card.encode('utf-8'))
    code.update('undetermined'.encode('utf-8'))
    code.update(data.API_KEY.encode('utf-8'))
    ###creating POST request
    data._post['timeOf'] = log_time
    data._post['plate'] = log_card
    data._post['hash'] = code.hexdigest()
    postfields = urlencode(data._post)
    ###requesting post
    buffer = BytesIO()
    c = pycurl.Curl() #constructor of curl instance
    c.setopt(c.URL, 'not-your-business') #destination address
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.POSTFIELDS, postfields)
    ###performing request
    print('Awaiting execution...')
    c.perform() #why so slowly?
    print('TIME: ', c.getinfo(c.TOTAL_TIME))
    c.close()
    print('Closing and decoding...')
    body = buffer.getvalue() #getting a response from server
    print('body: ', body)
    serv_resp = body.decode('utf-8')
    print('serv_resp: ', serv_resp)
    ###checking and opening door
    if '"GRANTED"' in serv_resp: #it's a string
        ###then we open
        comm_lib.ControlDevice(dev_handle, 1, 1, 2, 6, 0, '') #oper_id, door_num, door_output_oper, oper, none, none
    else:
        pass


    #logger.write('\n')
    #logger.write(repr(rt_log.value))
if __name__ == '__main__':
    logger = open('log.txt', 'a+') #defining a file with logs