# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.contrib.auth.models import User

ORDER_STATUSES = (
    # (0, 'created by passenger'),
    (1, 'waiting'),
    (2, 'accepted by taxi driver'),
    # (3, 'delivering'),
    (4, 'delivered'),
    (5, 'canceled by passenger'),
    # (6, 'canceled by taxi driver'),
    (10, 'deleted'),
)


class TaxiDriver(User):
    """
    TaxiDrivers.
    Drivers deliver passengers to the right places.
    """
    geo_position = models.PointField(max_length=42, null=True, blank=True, srid=4326)
    is_busy = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.username)


class Passenger(User):
    """
    Passengers.
    Passengers make orders.
    """

    def __unicode__(self):
        return unicode(self.username)


class Order(models.Model):
    """
    Orders.
    Created by passengers. Processed by drivers.
    """
    passenger = models.ForeignKey(Passenger, null=False, related_name='passenger')
    taxi_driver = models.ForeignKey(TaxiDriver, null=True, related_name='taxi_driver')

    geo_position = models.PointField(max_length=42, null=True, blank=True, srid=4326)
    start_ride_datetime = models.DateTimeField(null=False)
    finish_ride_datetime = models.DateTimeField(null=False)

    status = models.PositiveIntegerField(default=0, choices=ORDER_STATUSES)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        order = super(Order, self).save(*args, **kwargs)
        OrderHistory.objects.create(order=order, action=order.action)


class OrderHistory(models.Model):
    """
    OrderHistory.
    Order's history.
    """
    order = models.ForeignKey(Order, null=False, related_name='order')
    action = models.PositiveIntegerField(default=0, blank=True, choices=ORDER_STATUSES)
    created = models.DateTimeField(auto_now_add=True)
