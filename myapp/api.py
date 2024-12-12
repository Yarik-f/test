import requests

class CruiseAPIHelper:
    def __init__(self, base_url="http://127.0.0.1:8000/api/"):
        self.base_url = base_url

    def make_request(self, method, endpoint, params=None, data=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, params=params, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Request Error: {str(e)}")

    def get_free_tickets(self, cruise_id):
        endpoint = f"free-tickets/{cruise_id}/"
        return self.make_request("GET", endpoint)

    def book_cruise(self, user_id, cruise_id, place_cabin_id, is_full_cabin_booking):
        endpoint = "/book-cruise/"
        data = {
            "user_id": user_id,
            "cruise_id": cruise_id,
            "place_cabin_id": place_cabin_id,
            "is_full_cabin_booking": is_full_cabin_booking
        }
        return self.make_request("POST", endpoint, data=data)

    def cancel_reservation(self, user_id, ticket_numbers):
        endpoint = "/cancel-reservation/"
        data = {
            "user_id": user_id,
            "ticket_numbers": ticket_numbers
        }
        return self.make_request("POST", endpoint, data=data)
