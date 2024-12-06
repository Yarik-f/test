# from django.shortcuts import render, get_object_or_404
# from myapp.models import Cruise, Ports_schedule
#
#
# def cruise_details(request):
#     cruise_id = request.GET.get('cruise_id')
#     if cruise_id:
#         cruise = get_object_or_404(Cruise, id=cruise_id)
#         print(cruise.ship.image_ship)
#         schedule = Ports_schedule.objects.filter(cruise=cruise).order_by('day_number')
#         return render(request, 'cruise/index.html',
#                       {
#                           'cruise': cruise,
#                           'schedule': schedule
#                       })
#     else:
#         cruises = Cruise.objects.all()
#         return render(request, 'cruise/index.html', {'cruises': cruises})
from rest_framework import viewsets
from .models import Ship
from .serialisers import ShipSerializer

class ShipViewSet(viewsets.ModelViewSet):
    queryset = Ship.objects.all()
    serializer_class = ShipSerializer
