from django.core.management.base import BaseCommand
from core.modbustcp.promodem.client import PromodemClient
from time import sleep
import logging

logger = logging.getLogger(__name__)


def turn_switch(host="192.168.2.55", bright=0, client=None):
    if client is None:
        client = PromodemClient(host=host, debug=False, auto_close=False)
    client.set_brightness(bright)
    # print(client.get_full_info())
    logger.info(client.get_full_info())
    return client


class Command(BaseCommand):
    help = 'Generates Fake data'
    
    def handle(self, *args, **options):
        client = turn_switch(host="192.168.2.55", bright=0)
        client2 = turn_switch(host="192.168.2.66", bright=0)
        # print(client.close())
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
        sleep(1)
        turn_switch(bright=1, client=client)
        turn_switch(bright=1, client=client2)
        
        print('GET: {}, WRITE: {}'.format(client.count_get + client2.count_get, client.count_write + client2.count_get))
        print(client.close())
        print(client2.close())
        # client = PromodemClient(host="192.168.1.42", debug=False)
        # client.set_brightness(1)
        # print(client.get_full_info())
        #
        # client.set_voltage_inversion(0)
        # print(client.get_full_info())
