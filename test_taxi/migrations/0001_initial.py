# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geo_position', django.contrib.gis.db.models.fields.PointField(srid=4326, max_length=42, null=True, blank=True)),
                ('start_ride_datetime', models.DateTimeField()),
                ('finish_ride_datetime', models.DateTimeField()),
                ('status', models.PositiveIntegerField(default=0, choices=[(1, b'waiting'), (2, b'accepted by taxi driver'), (4, b'delivered'), (5, b'canceled by passenger'), (10, b'deleted')])),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.PositiveIntegerField(default=0, blank=True, choices=[(1, b'waiting'), (2, b'accepted by taxi driver'), (4, b'delivered'), (5, b'canceled by passenger'), (10, b'deleted')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(related_name='order', to='test_taxi.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='TaxiDriver',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('geo_position', django.contrib.gis.db.models.fields.PointField(srid=4326, max_length=42, null=True, blank=True)),
                ('is_busy', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='passenger',
            field=models.ForeignKey(related_name='passenger', to='test_taxi.Passenger'),
        ),
        migrations.AddField(
            model_name='order',
            name='taxi_driver',
            field=models.ForeignKey(related_name='taxi_driver', to='test_taxi.TaxiDriver', null=True),
        ),
    ]
