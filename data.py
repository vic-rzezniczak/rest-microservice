_post = { ### sample query structure
    'timeOf': '2017-04-23 21:12:17', ### sample
    'identifier': 'wiktor-src',
    'source': 'phpstorm',
    'plate': '2342794197', ### sample
    'direction': 'undetermined',
    'hash': '6e320431b2abd54033f07e364bba838b' ### sample
    }

_dev_addr = b'protocol=TCP, ipaddress=192.168.9.41, port=4370,t imeout=2000, passwd='
_server_addr = 'http://lpr-demo.vcn.pl/api/events/add'
_dev = None ### device handle
_comm = None ### dll handle
_line = ''
_time = ''
_card = ''
_resp = ''

API_KEY = '098f6bcd4621d373cade4e832627b4f6'