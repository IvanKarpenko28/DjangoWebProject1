# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-12-09 18:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0003_auto_20211209_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='клиент'),
        ),
    ]
