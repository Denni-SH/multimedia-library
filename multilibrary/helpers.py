
def generate_response(status=False, payload=None):

    return {
        'is_successful': status,
        'payload': payload
    }
