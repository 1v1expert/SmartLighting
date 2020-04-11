from django.core.management.base import BaseCommand
# from core.modbustcp.promodem.client import PromodemClient
from core.models import Promodem
from time import sleep
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Periodic get data from devices'
    
    def handle(self, *args, **options):
        devices = Promodem.objects.all()
        
        for device in devices:
            client = device.get_client()
            brightness = client.get_brightness()
            wifi_signal = client.get_wifi_signal()
            print(device, brightness, wifi_signal)
            if brightness is not None:
                client.brightness = brightness
                device.brightness = brightness
                device.save()
                
            if wifi_signal is not None:
                client.wifi_signal = wifi_signal
                device.wifi_signal = wifi_signal
                device.save()

