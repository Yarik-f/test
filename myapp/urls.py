from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShipViewSet, PassengerViewSet
from . import views, api_test

router = DefaultRouter()
router.register(r'ships', ShipViewSet)
router.register(r'passenger', PassengerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test/<slug:name>', api_test.test)
]