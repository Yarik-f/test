import json

from myapp.services import get_free_tickets_by_cruise


class CruiseAPIHelper:
    def get_free_tickets(self, cruise_id):
        try:
            result, total_free_place, total_free_cabin = get_free_tickets_by_cruise(cruise_id)

            response = {
                "result": result,
                "summary": {
                    "total_free_place": total_free_place,
                    "total_free_cabin": total_free_cabin
                }
            }
            return json.dumps(response)
        except Exception as e:

            error_response = {
                "error": str(e)
            }
            return json.dumps(error_response)