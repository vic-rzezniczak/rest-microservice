_POST = { ### sample query structure
    'timeOf': '2017-04-23 21:12:17', ### sample
    'identifier': 'wiktor-src',
    'source': 'phpstorm',
    'plate': '2342794197', ### sample
    'direction': 'undetermined',
    'hash': '6e320431b2abd54033f07e364bba838b' ### sample
    }

_DEV_ADDR = b'protocol=TCP, ipaddress=192.168.9.41, port=4370,t imeout=2000, passwd='
_SERVER_ADDR = 'http://lpr-demo.vcn.pl/api/events/add'
_DEV = None ### device handle
_COMM_LIB = None ### dll handle
_LOG = ''
_LINE = ''
_TIME = ''
_CARD = ''
_RESP = {}

API_KEY = '098f6bcd4621d373cade4e832627b4f6'