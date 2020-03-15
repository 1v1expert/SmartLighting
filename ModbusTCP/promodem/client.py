from ModbusTCP.core.client import ModbusClient
from retry import retry_call
import traceback


class WriteErrorException(Exception):
    """ Buffer error. """
    
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


class PromodemClient(object):
    
    """ Promodem TCP Client"""
    
    ATTEMPTS = 3
    
    def __init__(self, host='localhost', port=502, unit_id=None, timeout=1.0,
                 debug=True, auto_open=True, auto_close=True):
        
        self.promodem = ModbusClient(host=host, port=port, unit_id=unit_id, timeout=timeout,
                                     debug=debug, auto_open=auto_open, auto_close=auto_close)
        self.brightness = None
        self.voltage_inversion = None
        self.threshold_brightness_level = None
        self.wifi_signal = None
        self.project_code = None
        self.modification_code = None
        self.voltage_inversion = None
        self.threshold_brightness_level = None
        self.register_values = None
        self.brightness_value_when_turned_on = None
        self.brightness_step = None
        self.minutes_to_brightness_reset = None
        self.brightness_after_reset = None
        
        self.count_get = 0
        self.count_write = 0
        
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
    
    def get_wifi_signal(self):
        """ Получить уровень принимаемого сигнала WiFi  """
        return self._get(self.promodem.read_holding_registers, 14)
    
    def get_project_code(self) -> int:
        """ ID: Код проекта  """
        return self._get(self.promodem.read_holding_registers, 15)
    
    def get_modification_code(self) -> int:
        """ ID: Код модификации  """
        return self._get(self.promodem.read_holding_registers, 16)
    
    def get_voltage_inversion(self):
        return self._get(self.promodem.read_holding_registers, 1)
    
    def get_threshold_brightness_level(self) -> int:
        """ Установить пороговый уровень яркости для автоматического срабатывания реле """
        return self._get(self.promodem.read_holding_registers, 2)
    
    def get_brightness(self) -> int:
        """ Получить яркость светильника  % 0…100 % """
        return self._get(self.promodem.read_holding_registers, 0)
    
    def get_register_values(self) -> list:
        """ Получить значение однобитовых регистров, хар-их состояние дискретных входов """
        return [self.get_register_value(0), self.get_register_value(1)]
    
    def get_register_value(self, number_register: int) -> dict:
        return {number_register: self._get(self.promodem.read_discrete_inputs, number_register)}
    
    def get_brightness_value_when_turned_on(self):
        """ Получить уровень Яркости 0…100% при включении """
        return self._get(self.promodem.read_holding_registers, 3)
    
    def get_brightness_step(self):
        """ Получить шаг изменения яркости, 0…100 % в секунду """
        return self._get(self.promodem.read_holding_registers, 4)
    
    def get_minutes_to_brightness_reset(self):
        """ Получить время через которое будет сброшена яркость на значение по умолчанию, 1…255 минут  """
        return self._get(self.promodem.read_holding_registers, 5)
    
    def get_brightness_after_reset(self):
        """ Получить яркость, которая будет установлена при отсутствии запроса на чтение/запись"""
        return self._get(self.promodem.read_holding_registers, 6)
    
    def get_full_info(self) -> dict:
        return {
            'brightness': self.get_brightness() if self.brightness is None else self.brightness,
            'threshold_brightness_level': self.get_threshold_brightness_level()
            if self.threshold_brightness_level is None else self.threshold_brightness_level,
            'voltage_inversion': self.get_voltage_inversion() if self.voltage_inversion is None
            else self.voltage_inversion,
            'modification_code': self.get_modification_code() if self.modification_code is None
            else self.modification_code,
            'project_code': self.get_project_code() if self.project_code is None else self.project_code,
            'wifi_signal': self.get_wifi_signal() if self.wifi_signal is None else self.wifi_signal,
            'register_value': self.get_register_values() if self.register_values is None else self.register_values,
            'brightness_value_when_turned_on': self.get_brightness_value_when_turned_on()
            if self.brightness_value_when_turned_on is None else self.brightness_value_when_turned_on,
            'brightness_step': self.get_brightness_step() if self.brightness_step is None else self.brightness_step,
            'minutes_to_reset_brightness': self.get_minutes_to_brightness_reset()
            if self.minutes_to_brightness_reset is None else self.minutes_to_brightness_reset,
            'brightness_after_reset': self.get_brightness_after_reset()
            if self.brightness_after_reset is None else self.brightness_after_reset
        }
    
    def _get(self, func, *value):
        
        func_name = traceback.extract_stack()[-2:][0][2]
        var_name = func_name[4:]
        
        def wrap():
            self.count_get += 1
            try:
                return func(*value)[0]
            except Exception as e:
                Exception("Func %s is not ok, data not received" % func_name)
                
            
        try:
            result = retry_call(wrap, tries=self.ATTEMPTS)
            if not getattr(self, var_name, None):
                setattr(self, var_name, result)
            return result
        except Exception as e:
            print(e)
            return None
        
    def _write_command(self, func, *value):
        # open or reconnect TCP to server
        
        def wrap():
            self.count_write += 1
            if not self.promodem.is_open():
                if not self.promodem.open():
                    self.promodem.close()
                    raise ConnectionError("Exception: promodem is closed")

            is_ok = func(*value)
            if not is_ok:
                raise WriteErrorException("Exception: write error")
        
        try:
            return retry_call(wrap, tries=self.ATTEMPTS)
        except Exception as e:
            print(e)
            return False
        

        
        

