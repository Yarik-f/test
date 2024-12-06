from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Ship)
class ShipAdmin(admin.ModelAdmin):
    pass

@admin.register(Specifications)
class SpecificationsAdmin(admin.ModelAdmin):
    pass

@admin.register(Additional_service)
class Additional_serviceAdmin(admin.ModelAdmin):
    pass
@admin.register(Booking_list)
class Booking_listAdmin(admin.ModelAdmin):
    pass

@admin.register(Booking_ship)
class Booking_shipAdmin(admin.ModelAdmin):
    pass

@admin.register(Cruise)
class CruiseAdmin(admin.ModelAdmin):
    pass

@admin.register(Port)
class PortAdmin(admin.ModelAdmin):
    pass
@admin.register(Routes)
class RoutesAdmin(admin.ModelAdmin):
    pass

@admin.register(Cabin)
class CabinAdmin(admin.ModelAdmin):
    pass

@admin.register(Place_cabin)
class Place_cabinAdmin(admin.ModelAdmin):
    pass

@admin.register(Additional_service_cruise)
class Additional_service_cruiseAdmin(admin.ModelAdmin):
    pass

@admin.register(Booking_cruise)
class Booking_cruiseAdmin(admin.ModelAdmin):
    pass
