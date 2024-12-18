import json
import requests

class CruiseAPIHelper:
    base_url = 'http://127.0.0.1:8000/'

    def _validate_int(self, value, field_name):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{field_name} должно быть положительным целым числом.")

    def _validate_string(self, value, field_name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} должно быть непустой строкой.")

    def _validate_ticket_number(self, value):
        if isinstance(value, str):
            return
        if isinstance(value, list) and all(isinstance(num, str) for num in value):
            return
        raise ValueError("ticket_numbers должен быть строкой или списком строк.")

    def _make_request(self, method, url, params=None, json_data=None):
        try:
            if method == 'GET':
                response = requests.get(url, params=params)
            elif method == 'POST':
                response = requests.post(url, json=json_data, params=params)
            else:
                raise ValueError("Метод запроса не поддерживается.")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Ошибка при выполнении запроса: {e}")
        except json.JSONDecodeError:
            raise ValueError("Ответ от сервера не является валидным JSON.")

    def get_free_tickets(self, cruise_id):
        self._validate_int(cruise_id, 'cruise_id')
        url = f'{self.base_url}api/cabins/free-tickets/{cruise_id}'
        return self._make_request('GET', url)
    def book(self, user_id, cruise_id, place_cabin_id, is_full_cabin_booking=False):
        self._validate_int(user_id, 'user_id')
        self._validate_int(cruise_id, 'cruise_id')
        self._validate_int(place_cabin_id, 'place_cabin_id')

        payload = {
            "user_id": user_id,
            "cruise_id": cruise_id,
            "place_cabin_id": place_cabin_id,
            "is_full_cabin_booking": is_full_cabin_booking
        }

        url = f'{self.base_url}api/bookings/book-cruise/'
        return self._make_request('POST', url, json_data=payload)

    def user(self, username):
        self._validate_string(username, 'username')
        payload = {
            "username": username
        }
        url = f'{self.base_url}api/bookings/'
        return self._make_request('GET', url, params=payload)

    def cancel(self, user_id, ticket_numbers):
        self._validate_int(user_id, 'user_id')
        self._validate_ticket_number(ticket_numbers)

        payload = {"user_id": user_id, "ticket_numbers": ticket_numbers}
        url = f'{self.base_url}api/bookings/cancel-reservation/'
        return self._make_request('POST', url, json_data=payload)


api_h = CruiseAPIHelper()

# print(api_h.get_free_tickets(1))
# print(api_h.book(1, 1, 463))
# print(api_h.user("Ярослав"))
# print(api_h.cancel(1, ["d9b31bfd-ef3b-40e5-951c-61412f66db72", "ea2eb4a2-91ea-4dba-b4be-19f4ff8e745c"]))