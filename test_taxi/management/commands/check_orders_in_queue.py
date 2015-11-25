# -*- coding: utf-8 -*-
"""@package docstring
Check orders with waiting status and turn it on.
"""
from datetime import datetime
from django.core.management.base import BaseCommand
from test_taxi.models import *


class Command(BaseCommand):
    help = 'Check orders with waiting status and turn it on if time has come'

    def handle(self, *args, **options):
        print "Start"

        for order in Order.objects.filter(status=1, start_ride_datetime__lte=datetime.now()):

            driver = TaxiDriver.objects.filter(is_busy=False).distance(order.geo_position).order_by('distance')[0]

            if not driver:
                print "Have no free taxi. Finish."
                return False

            order.taxi_driver = driver
            order.status = 2
            order.save()

            driver.is_busy = True
            driver.save(update_fields=["is_busy"])

            # notify passenger that taxi is coming
            # notify taxi driver that he has a job

            # make delivered state
            order.status = 4
            order.save(update_fields=["status"])
            # make taxi driver free
            driver.is_busy = False
            driver.save(update_fields=["is_busy"])

            # then delete the order
            order.delete()
            order.save(update_fields=["status"])

        print "Finish"