from django.core.management.base import BaseCommand
from ModbusTCP.core.client import ModbusClient
from ModbusTCP.promodem.app import start
from ModbusTCP.promodem.client import PromodemClient

class Command(BaseCommand):
    help = 'Generates Fake data'
    
    def handle(self, *args, **options):
        client = PromodemClient(host="192.168.1.41")
        client.set_brightness(100)
        signal = client.get_wifi_signal()
        project_code = client.get_project_code()
        voltage_inversion = client.get_voltage_inversion()
        
        print(signal[0], project_code[0], bool(voltage_inversion[0]))
        client.set_voltage_inversion(0)
        voltage_inversion = client.get_voltage_inversion()
        print(bool(voltage_inversion[0]))
        # print(type())
        # start()
        # https://github.com/sourceperl/pyModbusTCP/tree/master/examples
        # c = ModbusClient(host="192.168.1.41", port=502, auto_open=True, auto_close=True, timeout=2, debug=True)
        # c.open()
        #
        # c.write_single_register(0, 0)
        # c.close()
