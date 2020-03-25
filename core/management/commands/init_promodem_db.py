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
        objs = []
        obj, created = Promodem.objects.get_or_create(ip=promodem["ip"], title=promodem["title"],
                                                      defaults={"created_by":User.objects.first(),
                                                                "updated_by": User.objects.first()})
        if created:
            objs.append(obj)
            
    Promodem.objects.bulk_create(objs)


class Command(BaseCommand):
    help = 'Init DB'
    
    def handle(self, *args, **options):
        filling_db()
