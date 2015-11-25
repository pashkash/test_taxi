"""@package docstring
Unit and funcs tests for Test_taxi api.
"""
import time

from rest_framework import status
from rest_framework.test import APITestCase
from django.test.utils import override_settings


class TestTaxiTests(APITestCase):
    """Test airport resource functionality."""
    fixtures = []  # data

