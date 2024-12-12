from django.db.models import Sum
from .models import Cabin, Place_cabin, Booking_cruise

def get_free_tickets_by_cruise(cruise_id):
    cabins = Cabin.objects.filter(ship__cruise__id=cruise_id)

    result = []
    total_free_place = 0
    total_free_cabin = 0

    for cabin in cabins:
        total_places = (
            Place_cabin.objects.filter(cabin=cabin)
            .aggregate(total=Sum('cabin__capacity'))['total'] or 0
        )

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

    return result, total_free_place, total_free_cabin