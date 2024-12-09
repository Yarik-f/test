from rest_framework import serializers
from .models import *

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__'
class ShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ship
        fields = '__all__'
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
class SpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specifications
        fields = '__all__'
class Additional_serviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Additional_service
        fields = '__all__'
class Booking_listSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking_list
        fields = '__all__'
class Booking_shipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking_ship
        fields = '__all__'
class CruiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cruise
        fields = '__all__'
        depth = 1
class PortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Port
        fields = '__all__'
class RoutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routes
        fields = '__all__'
class CabinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabin
        fields = '__all__'
class Place_cabinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place_cabin
        fields = '__all__'
class Additional_service_cruiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Additional_service_cruise
        fields = '__all__'
class Booking_cruiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking_cruise
        fields = '__all__'