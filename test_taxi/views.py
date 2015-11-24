from rest_framework import viewsets
from rest_framework.decorators import list_route, permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .api_serializers import *
from .models import *
from rest_framework import filters
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth import authenticate


class TaxiDriverViewSet(viewsets.ViewSet):
    # queryset = TaxiDriver.objects.all()
    # serializer_class = TaxiDriverSerializer

    @list_route(methods=['post'])
    def update_geoposition(self, request):
        """Send geoposition of taxi driver to the server.
        ---
        parameters_strategy: replace
        parameters:
            - name: id
              required: true
              defaultValue: 1
              description: id of taxi driver account
              paramType: form
              type: int
            - name: lat
              required: true
              defaultValue: 52.522906
              description: latitude
              paramType: form
              type: float
            - name: lon
              required: true
              defaultValue: 13.41156
              description: longitude
              paramType: form
              type: float
        response_serializer: CommonSerializer
        """
        driver_id, lat, lon = request.POST.get("id", None), request.POST.get("lat", None), request.POST.get("lon", None)

        if not all([driver_id, lat, lon]):
            return Response(CommonSerializer({"success": False, 'reason': 'Not enough params'}).data)

        try:
            driver = TaxiDriver.objects.get(id=driver_id)
            driver.geo_position.latitude = 0
            driver.geo_position.longitude = 0
            driver.save()

            return Response(CommonSerializer({"success": True, 'reason': ''}).data)

        except TaxiDriver.DoesNotExist:
            return Response(CommonSerializer({"success": False, 'reason': 'Taxi driver with this id doesnt exist'}).data)


class OrderViewSet(viewsets.ViewSet):
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer

    @list_route(methods=['post'])
    def create_order(self, request):
        """Send geoposition of passenger and time for deliver.
        ---
        parameters_strategy: replace
        parameters:
            - name: id
              required: true
              defaultValue: 1
              description: id of passenger account
              paramType: form
              type: int
            - name: lat
              required: true
              defaultValue: 52.522906
              description: latitude
              paramType: form
              type: float
            - name: lon
              required: true
              defaultValue: 13.41156
              description: longitude
              paramType: form
              type: float
            - name: start_ride_datetime
              required: false
              defaultValue:
              description: datetime for starting the deliver
              paramType: form
              type: datetime

        response_serializer: CommonSerializer
        """
        passenger_id, lat, lon, start_ride_datetime = request.POST.get("id", None), request.POST.get("lat", None), \
            request.POST.get("lon", None), request.POST.get("start_ride_datetime", None)

        if not all([passenger_id, lat, lon]):
            return Response(CommonSerializer({"success": False, 'reason': 'Not enough params'}).data)

        try:
            passenger = Passenger.objects.get(id=passenger_id)

            # find nearest driver
            # make order
            # make history

            return Response(CommonSerializer({"success": True, 'reason': ''}).data)

        except TaxiDriver.DoesNotExist:
            return Response(CommonSerializer({"success": False,
                                              'reason': 'Taxi driver with this id does not exist'}).data)


    @list_route(methods=['post'])
    def cancel_order(self, request):
        pass
        # cancel order
        # make history
