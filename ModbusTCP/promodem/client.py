from ModbusTCP.core.client import ModbusClient


class PromodemClient(object):
    
    """ Promodem TCP Client"""
    
    ATTEMPTS = 3
    
    def __init__(self, host='localhost', port=502, unit_id=None, timeout=1.0,
                 debug=True, auto_open=True, auto_close=True):
        
        self.promodem = ModbusClient(host=host, port=port, unit_id=unit_id, timeout=timeout,
                                     debug=debug, auto_open=auto_open, auto_close=auto_close)
    
    def set_brightness(self, value: int) -> bool:
        """ Установить яркость светильника
            Modbus function WRITE_SINGLE_REGISTER (0x06) | DEC=0, | reg_value
        """
        return self._write_command(self.promodem.write_single_register, 0, value)
    
    def set_voltage_inversion(self, value):
        """ Установить инверсию напряжения """
        return self._write_command(self.promodem.write_single_register, 1, int(bool(value)))
    
    def get_wifi_signal(self):
        """ Получить уровень принимаемого сигнала WiFi  """
        # return self.promodem.read_coils(14)
        return self.promodem.read_holding_registers(14)
    
    def get_project_code(self):
        """ ID: Код проекта  """
        return self.promodem.read_holding_registers(15)
    
    def get_modification_code(self):
        """ ID: Код модификации  """
        return self.promodem.read_holding_registers(16)
    
    def get_voltage_inversion(self):
        return self.promodem.read_holding_registers(1)
    
    def _write_command(self, func, *value):
        # open or reconnect TCP to server
        self.promodem.open()
        
        for i in range(self.ATTEMPTS):
            if not self.promodem.is_open():
                if not self.promodem.open():
                    continue

            if self.promodem.is_open():
                is_ok = func(*value)
                if is_ok:
                    return True
                
        return False
        
        

