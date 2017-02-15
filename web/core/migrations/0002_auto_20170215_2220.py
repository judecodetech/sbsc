# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 20:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suspect',
            name='eyebrow',
            field=models.CharField(choices=[(b'Bushy', b'bushy'), (b'Thick', b'thick'), (b'Raised', b'raised'), (b'Pencilled', b'pencilled')], default=b'Bushy', max_length=15),
        ),
    ]
