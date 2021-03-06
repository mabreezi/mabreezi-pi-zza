# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-05 07:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=300)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=6)),
                ('qrcode', models.ImageField(blank=True, null=True, upload_to='qrcode')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('role', models.CharField(choices=[('refugee', 'Refugee'), ('vendor', 'Vendor'), ('distributor', 'Distributor'), ('implementor', 'Implementing Partner')], max_length=20)),
                ('balance', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipment_id', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
        ),
    ]
