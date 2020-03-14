from django.core.management.base import BaseCommand
from ModbusTCP.core.client import ModbusClient
from ModbusTCP.promodem.app import start
from ModbusTCP.promodem.client import PromodemClient
from time import sleep


def turn_switch(host="192.168.1.42", bright=0, client=None):
    if client is None:
        client = PromodemClient(host=host, debug=False)
    client.set_brightness(bright)
    print(client.get_full_info())
    return client


class Command(BaseCommand):
    help = 'Generates Fake data'
    
    def handle(self, *args, **options):
        client = turn_switch(host="192.168.1.42", bright=0)
        client2 = turn_switch(host="192.168.1.41", bright=0)
        sleep(1)
        turn_switch(bright=0, client=client)
        turn_switch(bright=1, client=client2)
        sleep(1)
        turn_switch(bright=1, client=client)
        turn_switch(bright=0, client=client2)
        sleep(1)
        turn_switch(bright=1, client=client)
        turn_switch(bright=1, client=client2)
        sleep(1)
        turn_switch(bright=0, client=client)
        turn_switch(bright=0, client=client2)
        # client = PromodemClient(host="192.168.1.42", debug=False)
        # client.set_brightness(1)
        # print(client.get_full_info())
        #
        # client.set_voltage_inversion(0)
        # print(client.get_full_info())
