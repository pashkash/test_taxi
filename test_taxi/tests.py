"""@package docstring
Unit and funcs tests for Test_taxi api.
"""
import time
import datetime
from django.core import management
from rest_framework import status
from rest_framework.test import APITestCase
from test_taxi.models import *
from random import randint
from django.utils import timezone


class TestTaxiTests(APITestCase):
    """Test airport resource functionality."""
    fixtures = ['fixture.json']  # data

    def custom_test(self):

        extra_minutes = 0
        for i in xrange(2, 6):
            url = "/api/v1/orders/create_order/"
            extra_minutes = extra_minutes + randint(1, 5)

            data = {"id": i, "lat": 52.522906 + i, "lon": 13.41156 + i,
                    'start_ride_datetime': (datetime.datetime.now() +
                        datetime.timedelta(minutes=extra_minutes)).strftime("%Y-%m-%dT%H:%M:%S") if i < 4 else ''}

            print data
            response = self.client.post(url, data)
            print response

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["success"], True)

        while Order.objects.filter(status=1):
            management.call_command('check_orders_in_queue', verbosity=0)
            time.sleep(10)

        self.assertEqual(1, 1)

