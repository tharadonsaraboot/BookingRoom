from django.contrib import admin
from .models import Room, Booking, PaymentSlip

admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(PaymentSlip)
