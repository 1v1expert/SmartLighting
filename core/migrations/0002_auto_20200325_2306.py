# Generated by Django 3.0.2 on 2020-03-25 23:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promodem',
            name='brightness',
            field=models.IntegerField(null=None, verbose_name=' Яркость светильника '),
        ),
        migrations.AlterField(
            model_name='promodem',
            name='brightness_after_reset',
            field=models.IntegerField(null=True, verbose_name='Дефолтная яркость'),
        ),
        migrations.AlterField(
            model_name='promodem',
            name='brightness_step',
            field=models.IntegerField(null=True, verbose_name=' Шаг изменения яркости '),
        ),
        migrations.AlterField(
            model_name='promodem',
            name='brightness_value_when_turned_on',
            field=models.IntegerField(null=True, verbose_name='Уровень Яркости 0…100% при включении '),
        ),
        migrations.AlterField(
            model_name='promodem',
            name='ip',
            field=models.GenericIPAddressField(verbose_name=' Ip-адрес '),
        ),
        migrations.AlterField(
            model_name='promodem',
            name='minutes_to_brightness_reset',
            field=models.IntegerField(null=True, verbose_name='Количество минут до сброса яркости на дефолт'),
        ),
        migrations.AlterField(
            model_name='promodem',
            name='modification_code',
            field=models.IntegerField(null=True, verbose_name=' Код модификации '),
        ),
        migrations.AlterField(
            model_name='promodem',
            name='project_code',
            field=models.IntegerField(null=True, verbose_name=' Код проекта '),
        ),
        migrations.AlterField(
            model_name='promodem',
            name='register_values',
            field=models.CharField(max_length=2, null=True, verbose_name=' Значения однобитовых регистров '),
        ),
        migrations.AlterField(
            model_name='promodem',
            name='threshold_brightness_level',
            field=models.IntegerField(null=True, verbose_name='Пороговый уровень яркости для автоматического срабатывания реле '),
        ),
        migrations.AlterField(
            model_name='promodem',
            name='voltage_inversion',
            field=models.BooleanField(null=True, verbose_name=' Инверсия напряжения '),
        ),
        migrations.AlterField(
            model_name='promodem',
            name='wifi_signal',
            field=models.IntegerField(null=True, verbose_name=' Уровень принимаемого сигнала WiFi '),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Когда создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Когда обновлено')),
                ('is_public', models.BooleanField(default=True, verbose_name='Опубликовано?')),
                ('deleted', models.BooleanField(default=False, editable=False, verbose_name='В архиве?')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Кем создано')),
                ('promodem', models.ManyToManyField(related_name='groups', to='core.Promodem')),
                ('updated_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Кем обновлено')),
            ],
            options={
                'verbose_name': 'Группа ',
                'verbose_name_plural': 'Группы ',
            },
        ),
    ]