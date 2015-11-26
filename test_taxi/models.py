# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib import admin

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

    objects = models.GeoManager()


admin.site.register(TaxiDriver)


class Passenger(User):
    """
    Passengers.
    Passengers make orders.
    """

    def __unicode__(self):
        return unicode(self.username)


admin.site.register(Passenger)


class Order(models.Model):
    """
    Orders.
    Created by passengers. Processed by drivers.
    """
    passenger = models.ForeignKey(Passenger, null=False, related_name='passenger')
    taxi_driver = models.ForeignKey(TaxiDriver, null=True, related_name='taxi_driver')

    geo_position = models.PointField(max_length=42, null=True, blank=True, srid=4326)
    start_ride_datetime = models.DateTimeField(null=False, db_index=True)

    status = models.PositiveIntegerField(default=0, choices=ORDER_STATUSES, db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        OrderHistory.objects.create(order_id=self.pk, action=self.status)

    objects = models.GeoManager()


admin.site.register(Order)


class OrderHistory(models.Model):
    """
    OrderHistory.
    Order's history.
    """
    order = models.ForeignKey(Order, null=False, related_name='order')
    action = models.PositiveIntegerField(default=0, blank=True, choices=ORDER_STATUSES, db_index=True)
    created = models.DateTimeField(auto_now_add=True)


admin.site.register(OrderHistory)
