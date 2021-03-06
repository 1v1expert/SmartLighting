from django.db import models
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
import uuid
import logging
from core.signals import change_state
from core.modbustcp.promodem.client import PromodemClient

logger = logging.getLogger(__name__)

User = get_user_model()


class Base(models.Model):
    """
    Абстрактная базовая модель
    """
    uid = models.UUIDField(verbose_name="Идентификатор", primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Когда создано")
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Кем создано", editable=False,
                                   related_name="+")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Когда обновлено")
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Кем обновлено", editable=False,
                                   related_name="+")
    is_public = models.BooleanField("Опубликовано?", default=True)
    deleted = models.BooleanField("В архиве?", default=False, editable=False)
    
    class Meta:
        abstract = True
        verbose_name = "Базовая модель "
        verbose_name_plural = "Базовые модели"


class Promodem(Base):
    title = models.CharField(verbose_name='Наименование', max_length=255)
    ip = models.GenericIPAddressField(verbose_name=' Ip-адрес ')
    port = models.CharField(default='502',
                            max_length=400,
                            help_text="for TCP and UDP enter network port as number "
                                      "(def. 502, for serial ASCII and RTU enter serial port (/dev/pts/13))")
    
    brightness = models.IntegerField(verbose_name=' Яркость светильника ', null=None)
    wifi_signal = models.IntegerField(verbose_name=' Уровень принимаемого сигнала WiFi ', null=True)
    project_code = models.IntegerField(verbose_name=' Код проекта ', null=True)
    modification_code = models.IntegerField(verbose_name=' Код модификации ', null=True)
    voltage_inversion = models.BooleanField(verbose_name=' Инверсия напряжения ', null=True)
    threshold_brightness_level = models.IntegerField(
        verbose_name='Пороговый уровень яркости для автоматического срабатывания реле ', null=True)
    register_values = models.CharField(verbose_name=' Значения однобитовых регистров ', max_length=2, null=True)
    brightness_value_when_turned_on = models.IntegerField(verbose_name='Уровень Яркости 0…100% при включении ', null=True)
    brightness_step = models.IntegerField(verbose_name=' Шаг изменения яркости ', null=True)
    minutes_to_brightness_reset = models.IntegerField(verbose_name='Количество минут до сброса яркости на дефолт', null=True)
    brightness_after_reset = models.IntegerField(verbose_name='Дефолтная яркость', null=True)
    
    objects = models.Manager()
    
    class Meta:
        verbose_name = "Промодем "
        verbose_name_plural = "Промодемы "
    
    def __str__(self):
        return f'{self.title} <{self.ip}>'
    
    def __init__(self, *args, **kwargs):
        super(Promodem, self).__init__(*args, **kwargs)
        self.__initial = self._dict
        
    def get_client(self):
        return PromodemClient(host=self.ip, debug=False)
    
    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        # is_create = kwargs.get('is_create')
        # if not is_create:
        change_state(self)
        super(Promodem, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                                           self._meta.fields])

# https://github.com/trombastic/PyScada
# https://pymodbus.readthedocs.io/


class Group(Base):
    title = models.CharField(verbose_name='Наименование', max_length=255)
    devices = models.ManyToManyField(Promodem, related_name='groups')

    objects = models.Manager()
    
    class Meta:
        verbose_name = "Группа "
        verbose_name_plural = "Группы "
