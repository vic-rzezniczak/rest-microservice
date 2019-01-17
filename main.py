import controller
import data



if __name__ == '__main__':
    log = open('log.txt', 'a+') #defining a file with logs
    data._DEV, data._COMM_LIB = controller.connect()
    while 1:
        data._TIME, data._CARD = controller.get_event(data._DEV, data._COMM_LIB)
        code = controller.hash_query(data._TIME, data._CARD, data.API_KEY)
        controller.perform_query(code)
        controller.contorl_device(data._RESP)
        log.write('\n' + repr(data._LOG.value))