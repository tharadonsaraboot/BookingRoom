from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Room(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField(max_length=200)
    beds = models.IntegerField()
    baths = models.IntegerField()
    size = models.IntegerField(help_text="Square footage of the room")
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    reviews_count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
        # Add more statuses as needed
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def clean(self):
        # Ensure that the start_date is before the end_date
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError('Check-out date must be after the check-in date.')

        # Ensure that the start_date is not in the past
        if self.start_date < timezone.now().date():
            raise ValidationError('Check-in date cannot be in the past.')

    def __str__(self):
        return f"{self.user.username} - {self.room.name} ({self.start_date} to {self.end_date})"

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Booking, self).save(*args, **kwargs)
    
class PaymentSlip(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    slip = models.ImageField(upload_to='payment_slips/')
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment Slip for Booking {self.booking} by {self.booking.user}"

# Don't forget to make and run migrations after modifying your models.
