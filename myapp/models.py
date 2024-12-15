import uuid
from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.db import models
import logging
logger = logging.getLogger(__name__)

class Passenger(models.Model):
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
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    region = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.CharField(max_length=500)

    class Meta:
        verbose_name = 'Круизы'
        verbose_name_plural = 'Круизы'

    def __str__(self):
        return self.name_cruise
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
class Cabin(models.Model):
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    type_cabin = models.CharField(max_length=50)
    description_cabin = models.CharField(max_length=500)
    capacity = models.IntegerField()
    count_free = models.IntegerField()
    price = models.IntegerField()
    photo_cabin = models.ImageField(upload_to='static/images/', blank=True, null=True, verbose_name='Cabin')

    class Meta:
        verbose_name = 'Каюта'
        verbose_name_plural = 'Каюта'

    def __str__(self):
        return f'Тип каюты: {self.type_cabin}/Цена за каюту: {self.price}/Вместимость {self.capacity}/ Кол-во свободных кают {self.count_free}'
class Place_cabin(models.Model):
    cabin = models.ForeignKey(Cabin, on_delete=models.CASCADE)
    number_cabin = models.IntegerField()
    count_free_place = models.IntegerField()

    class Meta:
        verbose_name = 'Место в каюте'
        verbose_name_plural = 'Место в каюте'

    def __str__(self):
        return f'Номер каюты {self.number_cabin}/ Кол-во мест в каюте {self.count_free_place}'
class Additional_service_cruise(models.Model):
    name_service = models.CharField(max_length=50)
    price_service = models.IntegerField()

    class Meta:
        verbose_name = 'Дополнительные услуги на крумзе'
        verbose_name_plural = 'Дополнительные услуги на крумзе'

    def __str__(self):
        return self.name_service
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




