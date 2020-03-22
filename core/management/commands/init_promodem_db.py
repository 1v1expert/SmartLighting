from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

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
        obj, created = Promodem.objects.get_or_create(ip=promodem["ip"], title=promodem["title"],
                                                      defaults={"created_by": User, "updated_by": User})
        if not created:
            continue

        client = PromodemClient(host=promodem["ip"])
        info = client.get_full_info()
        
        for key in info.keys():
            if key == 'register_values':
                obj.register_values = '%d%d' % (info[key][0], info[key][1])
                continue
            if getattr(obj, key):
            
            
        
        


class Command(BaseCommand):
    help = 'Init DB'
    
    def handle(self, *args, **options):
        pass
