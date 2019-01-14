import ctypes
import hashlib
import requests as r

import controller
import data


input('\nShall I start?')

data._comm, data._dev = controller.connect()

while 1:
    data._time, data._card = controller.get_event(data._comm, data._dev)
    print(f'TIME: {data._time}, CARD: {data._card}')    
    ###if len(log_card) > 1: #we've got positive event
    ###print('\nTIME: ', log_time, '\tCARD: ', log_card)
    ###hashing
    code = hashlib.md5() #making a hash code instance
    code.update(data._time.encode('utf-8'))
    code.update('not-your-business'.encode('utf-8')) ### 'wiktor-src'
    code.update('phpstorm'.encode('utf-8'))
    code.update(data._card.encode('utf-8'))
    code.update('undetermined'.encode('utf-8'))
    code.update(data.API_KEY.encode('utf-8'))
    ###creating POST request
    data._post['timeOf'] = data._time
    data._post['plate'] = data._card
    data._post['hash'] = code.hexdigest()
    request = r.post(data._server_addr, data._post) ### destination address, post data
    data._resp = request.json()
    print(f'Response: {data._resp}')
    ###checking and opening door
    if data._resp['access'] == 'GRANTED':
        '''we open the door'''
        data._comm.ControlDevice(data._dev, 1, 1, 2, 6, 0, '') #oper_id, door_num, door_output_oper, oper, none, none
    else: pass


    #logger.write('\n')
    #logger.write(repr(rt_log.value))
if __name__ == '__main__':
    logger = open('log.txt', 'a+') #defining a file with logs