import json
import requests

class CruiseAPIHelper:
    def get_free_tickets(self, a):
        payload = f'{str(a)}'
        r = requests.get(f'http://127.0.0.1:8000/api/cabins/free-tickets/{payload}')
        return r.json(), r.url

    def book(self, user_id, cruise_id, place_cabin_id, is_full_cabin_booking=None):
        payload = {"user_id": "1", "cruise_id": "1", "place_cabin_id": "4"}
        r = requests.post('http://127.0.0.1:8000/api/bookings/book-cruise/', params=payload)
        return r.json(), r.url

    def user(self, username):
        payload = {"username": username}
        r = requests.get('http://127.0.0.1:8000/api/bookings/', params=payload)
        return r.json(), r.url

    def cancel(self, user_id, ticket_numbers):
        payload = {"user_id": user_id, "ticket_numbers": ticket_numbers}
        r = requests.post('http://127.0.0.1:8000/api/bookings/cancel-reservation/', params=payload)
        return r.json(), r.url


api_h = CruiseAPIHelper()

print(api_h.cancel("1", "c8c79eeb-9351-4eb5-9d7e-005c139dbff5"))