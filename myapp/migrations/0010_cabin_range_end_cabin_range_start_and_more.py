# Generated by Django 4.2.16 on 2024-12-17 08:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_booking_ship_number_booking_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cabin',
            name='range_end',
            field=models.IntegerField(blank=True, null=True, verbose_name='Конечный номер каюты'),
        ),
        migrations.AddField(
            model_name='cabin',
            name='range_start',
            field=models.IntegerField(blank=True, null=True, verbose_name='Начальный номер каюты'),
        ),
        migrations.AlterField(
            model_name='booking_ship',
            name='number_booking',
            field=models.UUIDField(default=uuid.UUID('2602fb3f-1d5f-4892-966b-351a9faf82b4'), editable=False),
        ),
        migrations.AlterField(
            model_name='cabin',
            name='capacity',
            field=models.IntegerField(verbose_name='Вместимость каюты'),
        ),
        migrations.AlterField(
            model_name='cabin',
            name='count_free',
            field=models.IntegerField(verbose_name='Количество свободных кают'),
        ),
        migrations.AlterField(
            model_name='cabin',
            name='description_cabin',
            field=models.CharField(max_length=500, verbose_name='Описание каюты'),
        ),
        migrations.AlterField(
            model_name='cabin',
            name='price',
            field=models.IntegerField(verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='cabin',
            name='type_cabin',
            field=models.CharField(max_length=50, verbose_name='Тип каюты'),
        ),
    ]
