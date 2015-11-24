# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import smart_unicode
from django.contrib.auth.models import User, UserManager
from geoposition.fields import GeopositionField

ORDER_STATUSES = (
    (0, 'created by passenger'),
    (1, 'waiting'),
    (2, 'accepted by taxi driver'),
    (3, 'delivering'),
    (4, 'delivered'),
    (10, 'deleted'),
)


class TaxiDriver(User):
    """
    TaxiDrivers.
    Drivers deliver passengers to the right places.
    """
    geo_position = GeopositionField(max_length=42, db_index=True, null=True, blank=True)

    # def get_full_name(self):
    #     pass
    #
    # def get_short_name(self):
    #     pass

    def __unicode__(self):
        return unicode(self.username)


class Passenger(User):
    """
    Passengers.
    Passengers make orders.
    """
    # def get_full_name(self):
    #     pass
    #
    # def get_short_name(self):
    #     pass

    # def __unicode__(self):
    #     return unicode(self.username)


class Order(models.Model):
    """
    Orders.
    Created by passengers. Processed by drivers.
    """
    passenger = models.ForeignKey(Passenger, null=False, related_name='passenger')
    taxi_driver = models.ForeignKey(TaxiDriver, null=True, related_name='taxi_driver')

    geo_position = GeopositionField(max_length=42, db_index=True, null=False)
    start_ride_datetime = models.DateTimeField(null=False)
    finish_ride_datetime = models.DateTimeField(null=False)

    status = models.PositiveIntegerField(default=0, blank=True, choices=ORDER_STATUSES)
    created = models.DateTimeField(auto_now_add=True)

    # def __unicode__(self):
    #     return smart_unicode(self.name)

    # def save(self):
    #     pass


class OrderHistory(models.Model):
    """
    OrderHistory.
    Order's history.
    """
    order = models.ForeignKey(Order, null=False, related_name='order')
    action = models.PositiveIntegerField(default=0, blank=True, choices=ORDER_STATUSES)
    created = models.DateTimeField(auto_now_add=True)
