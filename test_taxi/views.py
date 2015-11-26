from datetime import datetime
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from .api_serializers import *
from django.contrib.gis.geos import fromstr


class TaxiDriverViewSet(viewsets.ViewSet):
    queryset = TaxiDriver.objects.all()
    serializer_class = TaxiDriverSerializer

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
            driver.geo_position = fromstr('POINT(' + lat + ' ' + lon + ')', srid=4326)
            driver.save()

            return Response(CommonSerializer({"success": True, 'reason': ''}).data)

        except TaxiDriver.DoesNotExist:
            return Response(
                CommonSerializer({"success": False, 'reason': 'Taxi driver with this id doesnt exist'}).data)


class OrderViewSet(viewsets.ViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @list_route(methods=['post'])
    def create_order(self, request):
        """Passenger can create the order.
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
              defaultValue: 2015-11-30 12:00:00
              description: datetime ('%Y-%m-%dT%H:%M:%S') for starting the deliver
              paramType: form
              type: datetime

        response_serializer: CommonSerializer
        """
        passenger_id, lat, lon, start_ride_datetime = request.POST.get("id", None), request.POST.get("lat", None), \
            request.POST.get("lon", None), request.POST.get("start_ride_datetime", None)

        if not all([passenger_id, lat, lon]):
            return Response(CommonSerializer({"success": False, 'reason': 'Not enough params'}).data)

        verified_start_ride_datetime = None
        if start_ride_datetime:
            try:
                verified_start_ride_datetime = datetime.strptime(start_ride_datetime, '%Y-%m-%dT%H:%M:%S')

                if verified_start_ride_datetime < datetime.now():
                    return Response(CommonSerializer({"success": False,
                                                      'reason': 'We want future datetime.'}).data)

            except ValueError:
                return Response(CommonSerializer({"success": False,
                                                  'reason': 'Wrong start_ride_datetime format.'}).data)

        try:
            passenger = Passenger.objects.get(id=passenger_id)

            # common params of the order
            order_params = {'passenger': passenger, 'geo_position': 'POINT(' + lat + ' ' + lon + ')',
                            'start_ride_datetime': datetime.now()}

            # make full order
            if not verified_start_ride_datetime:
                # get nearest taxi driver
                ref_location = fromstr('POINT(' + lat + ' ' + lon + ')', srid=4326)
                driver = TaxiDriver.objects.filter(is_busy=False).distance(ref_location).order_by('distance')[0]

                if not driver:
                    return Response(CommonSerializer({"success": False, 'reason': 'Have not free taxi divers.'}).data)

                order_params['taxi_driver'] = driver
                order_params['status'] = 2
                order = Order.objects.create(**order_params)
                driver.is_busy = True
                driver.save()

                # send push message (we need token device id) to the taxi driver about the new Order
                # make delivered state
                order.status = 4
                order.save(update_fields=["status"])

                # make taxi driver free
                driver.is_busy = False
                driver.save(update_fields=["is_busy"])

                # then delete the order
                # order.delete()

            # make queued order
            else:
                order_params['status'] = 1
                order_params['start_ride_datetime'] = verified_start_ride_datetime
                # print verified_start_ride_datetime
                Order.objects.create(**order_params)

            return Response(CommonSerializer({"success": True, 'reason': ''}).data)

        except Passenger.DoesNotExist:
            return Response(CommonSerializer({"success": False,
                                              'reason': 'Passenger with this id does not exist'}).data)

    @list_route(methods=['post'])
    def cancel_order(self, request):
        """Passenger can cancel the order.
        ---
        parameters_strategy: replace
        parameters:
            - name: passenger_id
              required: true
              defaultValue: 1
              description: id of passenger account
              paramType: form
              type: int
            - name: order_id
              required: true
              defaultValue: 1
              description: order id
              paramType: form
              type: int

        response_serializer: CommonSerializer
        """
        passenger_id, order_id = request.POST.get("passenger_id", None), request.POST.get("order_id", None)

        if not all([passenger_id, order_id]):
            return Response(CommonSerializer({"success": False, 'reason': 'Not enough params'}).data)

        try:
            passenger = Passenger.objects.get(id=passenger_id)
            try:
                order = Order.objects.get(id=order_id, passenger=passenger, status__in=[0, 1, 2, 3])

                order.status = 5
                order.save(update_fields=["status"])

                # make taxi driver free
                if order.taxi_driver:
                    order.taxi_driver.is_busy = False
                    order.taxi_driver.save(update_fields=["is_busy"])

                return Response(CommonSerializer({"success": True, 'reason': ''}).data)

            except Order.DoesNotExist:
                return Response(CommonSerializer({"success": False, 'reason': 'Wrong order id'}).data)
        except Passenger.DoesNotExist:
            return Response(CommonSerializer({"success": False, 'reason': 'Wrong passenger id'}).data)
