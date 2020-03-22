from django.db import models
from django.contrib.auth import get_user_model
import uuid
import logging

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
    ip = models.GenericIPAddressField()
    port = models.CharField(default='502',
                            max_length=400,
                            help_text="for TCP and UDP enter network port as number "
                                      "(def. 502, for serial ASCII and RTU enter serial port (/dev/pts/13))")
    
    brightness = models.IntegerField(verbose_name=' Яркость светильника ')
    wifi_signal = models.IntegerField(verbose_name=' Уровень принимаемого сигнала WiFi ')
    project_code = models.IntegerField(verbose_name=' Код проекта ')
    modification_code = models.IntegerField(verbose_name=' Код модификации ')
    voltage_inversion = models.BooleanField(verbose_name=' Инверсия напряжения ')
    threshold_brightness_level = models.IntegerField(
        verbose_name='Пороговый уровень яркости для автоматического срабатывания реле ')
    register_values = models.CharField(verbose_name=' Значения однобитовых регистров ', max_length=2)
    brightness_value_when_turned_on = models.IntegerField(verbose_name='Уровень Яркости 0…100% при включении ')
    brightness_step = models.IntegerField(verbose_name=' Шаг изменения яркости ')
    minutes_to_brightness_reset = models.IntegerField(verbose_name='Количество минут до сброса яркости на дефолт')
    brightness_after_reset = models.IntegerField(verbose_name='Дефолтная яркость')
    
    class Meta:
        verbose_name = "Промодем "
        verbose_name_plural = "Промодемы "
    
    def __str__(self):
        return f' промодем {self.title} <{self.ip}>'

# https://github.com/trombastic/PyScada
# https://pymodbus.readthedocs.io/

