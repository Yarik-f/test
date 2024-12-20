import uuid
from datetime import timedelta

from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

class Passenger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    passport_number = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Пассажиры'
        verbose_name_plural = 'Пассажиры'

    def __str__(self):
        return self.name+self.last_name
class Category(models.Model):
    category = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'

    def __str__(self):
        return self.category
class Ship(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name_ship = models.CharField(max_length=50)
    image_ship = models.ImageField(upload_to='static/images/', blank=True, null=True, verbose_name='Ship')

    class Meta:
        verbose_name = 'Корабли'
        verbose_name_plural = 'Корабли'

    def __str__(self):
        return self.name_ship
class Specifications(models.Model):
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    count_cabins = models.IntegerField()
    year_of_release = models.DateTimeField()
    length = models.IntegerField()
    width = models.IntegerField()
    engine_power = models.IntegerField()
    description_ship = models.CharField(max_length=500)

    class Meta:
        verbose_name = 'Характеристики'
        verbose_name_plural = 'Характеристики'

    def __str__(self):
        return f'{self.year_of_release} / {self.length} / {self.description_ship}'
class Additional_service(models.Model):
    name_service = models.CharField(max_length=50)
    description_service = models.CharField(max_length=100)
    price_service = models.IntegerField()

    class Meta:
        verbose_name = 'Дополнительные услуги'
        verbose_name_plural = 'Дополнительные услуги'

    def __str__(self):
        return self.name_service
class Booking_list(models.Model):
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    rental_period = models.IntegerField()
    rental_price = models.IntegerField()

    class Meta:
        verbose_name = 'Сведения аренды лодки'
        verbose_name_plural = 'Сведения аренды лодки'

    def __str__(self):
        return f'{self.rental_period} / {self.rental_price}'
class Booking_ship(models.Model):
    number_booking = models.UUIDField(default=uuid.uuid4(), editable=False)
    user = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)# Booking_list добавить вместо коробля
    count_day = models.IntegerField()
    service = models.ForeignKey(Additional_service, on_delete=models.CASCADE)
    price = models.IntegerField()
    status = models.BooleanField()

    class Meta:
        verbose_name = 'Аренда лодок'
        verbose_name_plural = 'Аренда лодок'

    def __str__(self):
        return f'{self.number_booking} / {self.price} / {self.status}'
class Cruise(models.Model):
    name_cruise = models.CharField(max_length=50)
    # ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    region = models.CharField(max_length=50)
    # start_date = models.DateTimeField()
    # end_date = models.DateTimeField()
    count_night = models.PositiveIntegerField()
    description = models.CharField(max_length=500)

    class Meta:
        verbose_name = 'Круизы'
        verbose_name_plural = 'Круизы'

    def __str__(self):
        return self.name_cruise
class Date_cruise(models.Model):
    cruise = models.ForeignKey(Cruise, on_delete=models.CASCADE)
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    period = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Дата круиза'
        verbose_name_plural = 'Дата круиза'

    def __str__(self):
        return f'{self.id} | {self.cruise} | {self.ship} | {self.date_start} | {self.date_end}'

@receiver(pre_save, sender=Date_cruise)
def create_date_cruise(sender, instance, **kwargs):
    if not instance.pk:
        count_night = instance.cruise.count_night
        date_start = instance.date_start
        period = instance.period

        pre_save.disconnect(create_date_cruise, sender=Date_cruise)
        try:
            with transaction.atomic():
                for i in range(period):
                    date_end = date_start + timedelta(days=count_night)

                    if i == 0:
                        instance.date_start = date_start
                        instance.date_end = date_end
                        instance.save()
                    else:
                        Date_cruise.objects.create(
                            cruise=instance.cruise,
                            ship=instance.ship,
                            date_start=date_start,
                            date_end=date_end,
                            period=period
                        )
                    date_start = date_end
        finally:
            pre_save.connect(create_date_cruise, sender=Date_cruise)

class Port(models.Model):
    name_port = models.CharField(max_length=50)
    country = models.CharField(max_length=50, blank=True)
    image_port = models.ImageField(upload_to='static/images/', blank=True, null=True, verbose_name='Port')

    class Meta:
        verbose_name = 'Порт'
        verbose_name_plural = 'Порт'

    def __str__(self):
        return f'{self.name_port}/{self.country}'
class Routes(models.Model):
    number_day = models.IntegerField()
    port = models.ForeignKey(Port, on_delete=models.CASCADE)
    cruise = models.ForeignKey(Cruise, on_delete=models.CASCADE)
    date = models.DateField(default='2025-01-01')
    arrival_time = models.TimeField(blank=True, null=True)
    departure_time = models.TimeField(blank=True, null=True)
    description_route = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Маршруты'
        verbose_name_plural = 'Маршруты'

    def __str__(self):
        return f"{self.cruise}/{self.number_day}"
class Additional_service_cruise(models.Model):
    name_service = models.CharField(max_length=50)
    price_service = models.IntegerField()

    class Meta:
        verbose_name = 'Дополнительные услуги на крумзе'
        verbose_name_plural = 'Дополнительные услуги на крумзе'

    def __str__(self):
        return self.name_service
class Cabin(models.Model):
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    type_cabin = models.CharField(max_length=50, verbose_name="Тип каюты")
    capacity = models.PositiveIntegerField(verbose_name="Вместимость каюты")
    count_free = models.PositiveIntegerField(blank=True, null=True, verbose_name="Количество свободных кают")
    price = models.IntegerField(verbose_name="Цена")
    range_start = models.PositiveIntegerField(null=True, blank=True, verbose_name="Начальный номер каюты")
    range_end = models.PositiveIntegerField(null=True, blank=True, verbose_name="Конечный номер каюты")
    description_cabin = models.TextField(max_length=1000, verbose_name="Описание каюты")
    photo_cabin = models.ImageField(upload_to='static/images/', blank=True, null=True, verbose_name='Cabin')

    class Meta:
        verbose_name = 'Каюта'
        verbose_name_plural = 'Каюта'

    def __str__(self):
        return f'Тип каюты: {self.type_cabin}/Цена за каюту: {self.price}/Вместимость {self.capacity}/ Кол-во свободных кают {self.count_free}'
@receiver(pre_save, sender=Cabin)
def process_cabin_data(sender, instance, **kwargs):
    range_start = instance.range_start if instance.range_start else 0
    range_end = instance.range_end if instance.range_end else 0
    count_cabin = range_end - range_start
    if count_cabin > 0:
        instance.count_free = count_cabin + 1
    else:
        instance.count_free = 0
class Place_cabin(models.Model):
    cabin = models.ForeignKey(Cabin, on_delete=models.CASCADE)
    number_cabin = models.IntegerField()
    count_free_place = models.IntegerField()

    class Meta:
        verbose_name = 'Место в каюте'
        verbose_name_plural = 'Место в каюте'

    def __str__(self):
        return f'{self.id} | Номер каюты {self.number_cabin}/ Кол-во мест в каюте {self.count_free_place}'
@receiver(post_save, sender=Cabin)
def create_place_for_cabin(sender, instance, created, **kwargs):
    if created:
        for number in range(instance.range_start, instance.range_end + 1):
            Place_cabin.objects.create(
                cabin=instance,
                number_cabin=number,
                count_free_place=instance.capacity
            )

    else:
        existing_number = Place_cabin.objects.filter(cabin=instance).values_list('number_cabin', flat=True)
        new_number_cabin = set(range(instance.range_start, instance.range_end + 1))
        number_to_delete = set(existing_number) - new_number_cabin
        Place_cabin.objects.filter(cabin=instance, number_cabin__in=number_to_delete).delete()

        numbers_to_add = new_number_cabin - set(existing_number)
        for number in numbers_to_add:
            Place_cabin.objects.create(
                cabin=instance,
                number_cabin=number,
                count_free_place=instance.capacity
            )
class Booking_cruise(models.Model):
    ticket_number = models.UUIDField(default=uuid.uuid4, editable=False)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    cruise = models.ForeignKey(Cruise, on_delete=models.CASCADE)
    place_cabin = models.ForeignKey(Place_cabin, on_delete=models.CASCADE)
    additional_service = models.ForeignKey(Additional_service_cruise, on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    date_booking = models.DateTimeField()
    status = models.CharField(max_length=50)
    is_full_cabin_booking = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Бронирование билета на круиз'
        verbose_name_plural = 'Бронирование билета на круиз'

    def __str__(self):
        return f'{self.ticket_number}'

    def save(self, *args, **kwargs):
        cabin_price = self.place_cabin.cabin.price if self.place_cabin and self.place_cabin.cabin else 0
        service_price = self.additional_service.price_service if self.additional_service else 0
        self.price = cabin_price + service_price

        try:
            with transaction.atomic():
                cabin = self.place_cabin.cabin

                if self.is_full_cabin_booking:
                    if cabin.count_free <= 0:
                        raise ValidationError("Нет свободных кают для бронирования")
                    cabin.count_free -= 1
                    self.place_cabin.count_free_place = 0
                    self.place_cabin.save()
                else:
                    if self.place_cabin.count_free_place <= 0:
                        raise ValidationError("Нет доступных мест в выбранной каюте")
                    self.place_cabin.count_free_place -= 1
                    self.place_cabin.save()

                    if self.place_cabin.count_free_place == 0:
                        if cabin.count_free > 0:
                            cabin.count_free -= 1

                cabin.save()
        except Exception as e:
            raise ValidationError(f"Ошибка при бронировании: {str(e)}")

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            cabin = self.place_cabin.cabin

            if self.is_full_cabin_booking:
                cabin.count_free += 1
                self.place_cabin.count_free_place = cabin.capacity
                self.place_cabin.save()
            else:
                self.place_cabin.count_free_place += 1
                self.place_cabin.save()

                if self.place_cabin.count_free_place == 1:
                    cabin.count_free += 1

            cabin.save()
        super().delete(*args, **kwargs)




