from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from django.http import HttpResponse

from rest_framework.exceptions import APIException

from . import serialisers, models

@api_view(['GET'])
def get_cruise(request):
    cruise = models.Cruise.objects.all()
    serialized_data = serialisers.CruiseSerializer(cruise, many=True).data
    return Response(serialized_data)