from rest_framework.views import exception_handler


def generate_formatted_response(status=False, payload=None):

    return {
        'status': status,
        'data': payload
    }


def exceptions_handler(exc, context):
    response = exception_handler(exc, context)
    if hasattr(response, 'data'):
        response.data = {
            'status': False,
            'data': {
                'message': response.data['detail']
                if hasattr(response, 'data') and response.data.get('detail')
                else 'Unexpected error!'
            }
        }

    return response
