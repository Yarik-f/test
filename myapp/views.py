import json

from django.db.models import Sum, Min
from django.utils import timezone

from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet
from .serialisers import *
from django.utils.timezone import now
from datetime import timedelta
from rest_framework.decorators import action
from rest_framework.response import Response



def cruise_details(request):
    return render(request, 'cruise/home.html')

def cruise(request):
    cruise_id = request.GET.get('cruise_id')
    if cruise_id:
        cruise = get_object_or_404(Cruise, id=cruise_id)
        # schedule = Ports_schedule.objects.filter(cruise=cruise).order_by('day_number')
        return render(request, 'cruise/cruise.html',
                      {
                          'cruise': cruise,

                          # 'schedule': schedule
                      })
    else:
        ship_with_cabin_price =[]
        route = Routes.objects.all()
        cruises = Cruise.objects.all()
        for cruise in cruises:
            min_price_cabin = Cabin.objects.filter(ship=cruise.ship).aggregate(Min('price'))['price__min']
            ship_with_cabin_price.append({
                'ship': cruise.ship,
                'min_price': min_price_cabin if min_price_cabin is not None else 'Нет кают'
            })

        # min_price_cabin = Cabin.objects.aggregate(Min('price'))['price__min']
        return render(request, 'cruise/cruise.html',
                      {
                          'cruises': cruises,
                          'ship_with_cabin_price': ship_with_cabin_price,
                          'route': route,
                       })


class ShipViewSet(ModelViewSet):
    queryset = Ship.objects.all()
    serializer_class = ShipSerializer
class PassengerViewSet(ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
class CruiseViewSet(ReadOnlyModelViewSet):
    queryset = Cruise.objects.all()
    serializer_class = CruiseSerializer

class CabinViewSet(ReadOnlyModelViewSet):
    queryset = Cabin.objects.all()
    serializer_class = CabinSerializer

    @action(detail=False, methods=['get'], url_path='free-tickets/(?P<cruise_id>[^/.]+)')
    def free_tickets(self, request, cruise_id=None):
        cabins = Cabin.objects.filter(ship__cruise__id=cruise_id)

        result = []
        total_free_place = 0
        total_free_cabin = 0
        for cabin in cabins:
            total_places = Place_cabin.objects.filter(cabin=cabin).aggregate(total=Sum('cabin__capacity'))['total'] or 0

            reserved_places_query = Booking_cruise.objects.filter(
                cruise_id=cruise_id,
                place_cabin__cabin=cabin,
                status__in=["reserved", "purchased"]
            )

            reserved_places = 0
            for booking in reserved_places_query:
                if booking.is_full_cabin_booking:
                    reserved_places += booking.place_cabin.cabin.capacity
                else:
                    reserved_places += 1

            free_places = total_places - reserved_places
            total_free_cabin += cabin.count_free
            total_free_place += free_places

            result.append({
                'cabin_type': cabin.type_cabin,
                'total_cabin': cabin.count_free,
                'total_places': total_places,
                'reserved_places': reserved_places,
                'free_places': max(0, free_places),
            })
        print(total_free_place)
        print(total_free_cabin)
        return Response(result)

class BookingCruiseViewSet(ViewSet):
    def list(self, request):
        username = request.query_params.get('username', None)

        if not username:
            return Response({"error": "Параметр 'username' обязателен"}, status=400)

        passenger = get_object_or_404(Passenger, name=username)
        bookings = Booking_cruise.objects.filter(passenger=passenger)

        serializer = Booking_cruiseSerializer(bookings, many=True).data
        return Response(serializer)

    @action(detail=False, methods=['post'], url_path='book-cruise')
    @transaction.atomic
    def book_cruise(self, request):
        user_id = request.query_params.get('user_id')
        cruise_id = request.query_params.get('cruise_id')
        place_cabin_id = request.query_params.get('place_cabin_id')
        is_full_cabin_booking = request.query_params.get('is_full_cabin_booking', False)

        if not all([user_id, cruise_id, place_cabin_id]):
            return Response({'status': 'Failed', 'message': "Параметры обязательны"}, status=400)

        try:
            passenger = Passenger.objects.get(id=user_id)
            cruise = Cruise.objects.get(id=cruise_id)
            place_cabin = Place_cabin.objects.select_for_update().get(id=place_cabin_id)
        except (Passenger.DoesNotExist, Cruise.DoesNotExist, Place_cabin.DoesNotExist) as e:
            return Response({'status': 'Failed', 'message': str(e)}, status=400)

        if place_cabin.count_free_place <= 0:
            return Response({'status': 'Failed', 'message': 'Нет доступных мест в выбранной каюте'}, status=400)

        cabin = place_cabin.cabin
        total_price = cabin.price

        if is_full_cabin_booking:
            reserved_places = cabin.capacity
        else:
            reserved_places = 1

        if is_full_cabin_booking and place_cabin.count_free_place < reserved_places:
            return Response({'status': 'Failed', 'message': 'Недостаточно мест для полной брони каюты'}, status=400)

        try:
            booking = Booking_cruise.objects.create(
                passenger=passenger,
                cruise=cruise,
                place_cabin=place_cabin,
                price=total_price,
                date_booking=timezone.now(),
                status='reserved',
                is_full_cabin_booking=is_full_cabin_booking
            )
        except ValidationError as e:
            return Response({'status': 'Failed', 'message': str(e)}, status=400)

        return Response({
            'status': 'OK',
            'type_cabin': cabin.type_cabin,
            'number_cabin': place_cabin.number_cabin,
            'reserved_places': reserved_places,
            'total_price': total_price,
            'booking_id': booking.id
        })

    @action(detail=False, methods=['post'], url_path='cancel-reservation')
    @transaction.atomic
    def cancel_reservation(self, request):

        user_id = request.query_params.get('user_id')
        ticket_numbers = request.query_params.get('ticket_numbers')

        if not user_id or not ticket_numbers:
            print(user_id)
            print(ticket_numbers)
            return Response({"status": "НЕ ОК", "error": "user_id и ticket_numbers обязательны"}, status=400)

        if isinstance(ticket_numbers, str):
            ticket_numbers = [ticket_numbers]

        if not isinstance(ticket_numbers, list):
            return Response({"status": "НЕ ОК", "error": "ticket_numbers должен быть строкой или списком"}, status=400)

        try:
            passenger = Passenger.objects.get(id=user_id)
        except Passenger.DoesNotExist:
            return Response({"status": "НЕ ОК", "error": "Пользователь не найден"}, status=404)

        bookings = Booking_cruise.objects.filter(
            passenger=passenger,
            ticket_number__in=ticket_numbers,
            status="reserved",
            cruise__start_date__gte=now() + timedelta(weeks=1)
        )

        if not bookings.exists():
            return Response({"status": "НЕ ОК", "error": "Нет подходящих броней для отмены"}, status=400)

        for booking in bookings:
            booking.delete()

        return Response({"status": "ОК", "message": "Бронь успешно снята"}, status=200)


