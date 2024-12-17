from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from .views import *
from django.contrib.auth import views as auth_views
router = DefaultRouter()
router.register(r'ships', ShipViewSet)
router.register(r'passenger', PassengerViewSet)
router.register(r'cruise', CruiseViewSet, basename='cruise')
router.register(r'cabins', CabinViewSet, basename='cabins')
router.register(r'bookings', BookingCruiseViewSet, basename='bookings')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', home_view, name='home'),
    path('cruise/', cruise_view, name='cruise'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', ProtectedView.as_view(), name='profile'),

    # path('cruise/', api_test.get_cruise)
]