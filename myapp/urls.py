from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShipViewSet
from . import views, api_test

router = DefaultRouter()
router.register(r'ships', ShipViewSet)

urlpatterns = [
    path('', include(router.urls)),
]