

def modify_reponse(response_instance):
    response_instance.pop('_state', None)
    response_instance.pop('password', None)
    response_instance.pop('is_superuser', None)
    response_instance.pop('is_staff', None)
    response_instance.pop('is_active', None)
    response_instance.pop('backend', None)
    return response_instance
