from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import models

from core.models import Promodem
from core.modbustcp.promodem.client import PromodemClient

User = get_user_model()

promodems = [
    {
        "ip": "192.168.2.55",
        "title": "promodem_v1",
    },
    {
        "ip": "192.168.2.66",
        "title": "promodem_v2",
    }]


def filling_db():
    for promodem in promodems:
        try:
            obj = Promodem.objects.get(ip=promodem["ip"], title=promodem["title"])
            continue  # not update
        except models.ObjectDoesNotExist:
            obj = Promodem(ip=promodem["ip"], title=promodem["title"])

        client = PromodemClient(host=promodem["ip"])
        info = client.get_full_info()
        
        print(info)
        
        for key in info.keys():
            if key == 'register_values':
                obj.register_values = '%d%d' % (info[key][0], info[key][1])
                continue
                
            if getattr(obj, key, None):
                setattr(obj, key, info[key])
            
            obj.save()
            

class Command(BaseCommand):
    help = 'Init DB'
    
    def handle(self, *args, **options):
        filling_db()
