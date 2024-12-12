from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from .views import *
from . import views, api_test

router = DefaultRouter()
router.register(r'ships', ShipViewSet)
router.register(r'passenger', PassengerViewSet)
router.register(r'cruise', CruiseViewSet)
router.register(r'cabins', CabinViewSet, basename='cabins')
router.register(r'bookings', BookingCruiseViewSet, basename='bookings')

urlpatterns = [
    path('', include(router.urls)),

    # path('cruise/', api_test.get_cruise)
]