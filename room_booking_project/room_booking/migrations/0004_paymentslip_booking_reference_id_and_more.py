# Generated by Django 5.0 on 2024-02-29 18:52

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_booking', '0003_paymentslip_guest_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentslip',
            name='booking_reference_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='paymentslip',
            name='checkin_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='paymentslip',
            name='checkout_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='paymentslip',
            name='guest_name',
            field=models.CharField(default=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL), max_length=255),
        ),
    ]