# Generated by Django 3.0.2 on 2020-04-01 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200325_2306'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='promodem',
            new_name='devices',
        ),
    ]