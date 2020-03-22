from django.db import models
from django.contrib.auth import get_user_model
import uuid

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
        
        
class PromodemClient(models.Model):
    pass
