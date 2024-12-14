# Generated by Django 4.2.16 on 2024-12-14 17:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='port',
            name='image_port',
            field=models.ImageField(blank=True, null=True, upload_to='static/images/', verbose_name='Port'),
        ),
        migrations.AlterField(
            model_name='booking_ship',
            name='number_booking',
            field=models.UUIDField(default=uuid.UUID('602fe215-0439-4b3e-ac7f-fc54a5be332a'), editable=False),
        ),
    ]
