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
    
    def set_voltage_inversion(self, value: int) -> bool:
        """ Установить инверсию напряжения """
        return self._write_command(self.promodem.write_single_register, 1, int(bool(value)))
    
    def set_threshold_brightness_level(self, value: int) -> bool:
        """ Установить пороговый уровень яркости для автоматического срабатывания реле """
        return self._write_command(self.promodem.write_single_register, 2, value)
    
    def get_wifi_signal(self) -> int:
        """ Получить уровень принимаемого сигнала WiFi  """
        # return self.promodem.read_coils(14)
        return self.promodem.read_holding_registers(14)[0]
    
    def get_project_code(self) -> int:
        """ ID: Код проекта  """
        return self.promodem.read_holding_registers(15)[0]
    
    def get_modification_code(self) -> int:
        """ ID: Код модификации  """
        return self.promodem.read_holding_registers(16)[0]
    
    def get_voltage_inversion(self):
        voltage_inversion = self.promodem.read_holding_registers(1)
        return voltage_inversion
    
    def get_threshold_brightness_level(self) -> int:
        """ Установить пороговый уровень яркости для автоматического срабатывания реле """
        return self.promodem.read_holding_registers(2)[0]

    def get_brightness(self) -> int:
        """ Получить яркость светильника  % 0…100 % """
        return self.promodem.read_holding_registers(0)[0]
    
    def get_register_values(self) -> list:
        """ """
        return [self.get_register_value(0), self.get_register_value(1)]
    
    def get_register_value(self, number_register: int) -> dict:
        return {number_register: self.promodem.read_discrete_inputs(number_register)[0]}
    
    def get_brightness_value_when_turned_on(self):
        return ''
    
    def get_full_info(self) -> dict:
        return {
            'brightness': self.get_brightness(),
            'threshold_brightness_level': self.get_threshold_brightness_level(),
            'voltage_inversion': self.get_voltage_inversion(),
            'modification_code': self.get_modification_code(),
            'project_code': self.get_project_code(),
            'wifi_signal': self.get_wifi_signal(),
            'register_value': self.get_register_values()
        }
    
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
        
        

