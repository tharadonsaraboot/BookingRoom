from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model

def get_default_username():
    return get_user_model().username

class Room(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='room_images/', null=True) # Define the image field
    beds = models.IntegerField()
    baths = models.IntegerField()
    size = models.IntegerField(help_text="Square footage of the room")
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    reviews_count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=255)
    checkin_date = models.DateField() 
    checkout_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # New field for storing calculated amount

    def __str__(self):
        return f"Booking {self.booking_id} - {self.room.name} by {self.user.username}"

    def save(self, *args, **kwargs):
        if self.checkin_date and self.checkout_date and self.room:
            duration = (self.checkout_date - self.checkin_date).days
            if duration < 0:
                raise ValidationError("Checkout date must be after checkin date")

            self.amount = duration * self.room.price

        super().save(*args, **kwargs)
    
class PaymentSlip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    slip = models.ImageField(upload_to='payment_slips/')
    verified = models.BooleanField(default=False)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    guest_name = models.CharField(max_length=255, default=get_default_username)
    booking_reference_id = models.IntegerField(default=0)
    checkin_date = models.DateField(default=timezone.now)
    checkout_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Payment Slip for {self.room} by {self.user}"