# Generated by Django 5.0 on 2024-02-29 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_booking', '0005_alter_paymentslip_guest_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='image_url',
        ),
        migrations.AddField(
            model_name='room',
            name='image',
            field=models.ImageField(null=True, upload_to='room_images/'),
        ),
    ]