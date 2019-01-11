from io import BytesIO
from urllib.parse import urlencode
from imp import reload
import ctypes
import sys
import parametres
import hashlib
import pycurl

import data


#code = hashlib.md5() #making a hash code instance
#buffer = BytesIO() #buffer for server response

logger = open('log.txt', 'a+') #defining a file with logs



              
# def TouchMeNow(): #library, connection parametres, dev data

print('HERE IS JOHHNY!', '\n')

###connecting to a library
comm_lib = ctypes.windll.LoadLibrary("plcommpro.dll")
print('\n', repr(comm_lib))

###connection parametres
dev_str = ctypes.create_string_buffer(b"protocol=TCP, ipaddress=192.168.9.41, port=4370,t imeout=2000, passwd=") #controller address
print('\n', repr(dev_str))

###connecting with device
dev_handle=comm_lib.Connect(dev_str)
print('\n', dev_handle)

###getting device information
info_buffer = ctypes.create_string_buffer(2048)
print('\nBuffer created')		
info_items = ctypes.create_string_buffer(b"DeviceID, Door1SensorType, Door1Drivertime, Door1Intertime") #dev_data
print('\nItems to obtain: ', info_items)
	
dev_info = comm_lib.GetDeviceParam(dev_handle, info_buffer, 256, info_items)
print('\nItems returned', dev_info)

print('\n', repr(info_buffer.value))

###opening doors	
comm_lib.ControlDevice(dev_handle, 1, 1, 2, 6, 0, '') #oper_id, door_num, door_output_oper, oper, none, none

input('\nShall I start?')

###starting to monitor reader states
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
    code.update('not-your-business'.encode('utf-8'))
    code.update('phpstorm'.encode('utf-8'))
    code.update(log_card.encode('utf-8'))
    code.update('undetermined'.encode('utf-8'))
    code.update('not-your-business'.encode('utf-8'))
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