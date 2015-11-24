from rest_framework import serializers
from .models import *


class TaxiDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxiDriver


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger


class OrderSerializer(serializers.ModelSerializer):
    passenger = TaxiDriverSerializer(read_only=True,)
    taxi_driver = PassengerSerializer(read_only=True,)

    class Meta:
        model = Order


class CommonSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=False, help_text="True if worked as planned.")
    reason = serializers.CharField(default=False, help_text="Contains the reason of failure.")