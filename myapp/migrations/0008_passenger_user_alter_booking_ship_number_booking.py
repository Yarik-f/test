# Generated by Django 4.2.16 on 2024-12-16 07:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0007_rename_arrival_date_routes_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='passenger',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='booking_ship',
            name='number_booking',
            field=models.UUIDField(default=uuid.UUID('337b17b5-0c36-4930-9699-e5e78899e2ab'), editable=False),
        ),
    ]
