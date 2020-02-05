from django.core.management.base import BaseCommand
from ModbusTCP.core.client import ModbusClient
from ModbusTCP.promodem.app import start

class Command(BaseCommand):
    help = 'Generates Fake data'
    
    def handle(self, *args, **options):
        start()
        # https://github.com/sourceperl/pyModbusTCP/tree/master/examples
        # c = ModbusClient(host="192.168.1.41", port=502, auto_open=True, auto_close=True, timeout=2, debug=True)
        # c.open()
        #
        # c.write_single_register(0, 0)
        # c.close()
