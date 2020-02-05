from ModbusTCP.core.client import ModbusClient

class PromodemClient(object):
    
    """ Promodem TCP Client"""
    
    def __init__(self, host='localhost', port=502, unit_id=None, timeout=1.0,
                 debug=True, auto_open=True, auto_close=True):
        
        self.promodem = ModbusClient(host=host, port=port, unit_id=unit_id, timeout=timeout,
                                     debug=debug, auto_open=auto_open, auto_close=auto_close)
    
    def set_brightness(self, value):
        """ Modbus function WRITE_SINGLE_REGISTER (0x06) | DEC=0, | reg_value """
        self.promodem.write_single_register(0, value)