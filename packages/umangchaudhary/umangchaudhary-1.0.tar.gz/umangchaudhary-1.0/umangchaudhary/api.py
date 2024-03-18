from typing import Any


class GenerateResponse:
    def generate_standard_response(self, success: int, messages: str, data: Any) -> dict:
        """
        :param success: 0, 1 indicating type of the request [ 0 for failed, 1 for success ]
        :param messages: api message
        :param data: data you want to return as response.
        :return: dict
            Sample response:
            {
                'success': 1,
                'message' : "request processed successfully."
                'data' : {'user_id' : 1, 'is_active': True}
            }
        """
        response = {
            "success": success,
            "message": messages if messages else ""
        }
        if data is not None:
            response["data"] = data
        return response
