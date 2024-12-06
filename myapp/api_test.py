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

@api_view(['GET', 'POST'])
def test(request, name):
    print(request.__dict__)
    print(request.GET)
    print(request.method)
    print(request.session)
    print(request._user)
    print(request.parser_context['kwargs'])
    print(name)
    data = models.Passenger.objects.all()
    serialized_data = serialisers.PassengerSerializer(data, many=True).data
    return Response(name)