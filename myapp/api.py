import json
import requests

class CruiseAPIHelper:
    base_url = 'http://127.0.0.1:8000/'

    def get_free_tickets(self, a):
        payload = f'{str(a)}'
        r = requests.get(f'{self.base_url}api/cabins/free-tickets/{payload}')
        return r.json()

    def book(self, user_id, cruise_id, place_cabin_id, is_full_cabin_booking=None):
        payload = {"user_id": "1", "cruise_id": "1", "place_cabin_id": "4"}
        r = requests.post(f'{self.base_url}api/bookings/book-cruise/', params=payload)
        return r.json()

    def user(self, username):
        payload = {"username": username}
        r = requests.get(f'{self.base_url}api/bookings/', params=payload)
        return r.json()

    def cancel(self, user_id, ticket_numbers):
        payload = {"user_id": user_id, "ticket_numbers": ticket_numbers}
        r = requests.post(f'{self.base_url}api/cancel-reservation/', params=payload)
        return r.json()


api_h = CruiseAPIHelper()

# print(api_h.get_free_tickets(1))
print(api_h.user("Ярослав"))