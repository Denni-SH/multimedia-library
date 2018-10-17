from rest_framework import status

from multilibrary.helpers import generate_formatted_response


class CommonExceptionHandler:

    @staticmethod
    def get_response_data_and_status(error=None):
        # TODO logger
        print(f'ERROR: {type(error)}')

        payload = error.message if hasattr(error, 'message') else str(type(error))
        response_status = error.status if hasattr(error, 'status') else status.HTTP_400_BAD_REQUEST
        response_data = generate_formatted_response(status=False, payload={"message": payload})

        return response_data, response_status
