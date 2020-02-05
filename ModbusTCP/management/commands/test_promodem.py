from django.core.management.base import BaseCommand
from ModbusTCP.core.client import ModbusClient
from ModbusTCP.promodem.app import start
from ModbusTCP.promodem.client import PromodemClient


class Command(BaseCommand):
    help = 'Generates Fake data'
    
    def handle(self, *args, **options):
        client = PromodemClient(host="192.168.1.41", debug=False)
        client.set_brightness(0)
        print(client.get_full_info())

        client.set_voltage_inversion(0)
        print(client.get_full_info())
