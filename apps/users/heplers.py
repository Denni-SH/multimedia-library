
def valid_mandatory_fields(data, fields=set()):
    """ Checks for missing/empty fields.
    """
    if not fields.issubset(set(data.keys())):
        return False

    present_fields = fields.intersection(set(data.keys()))
    values_fields = {data[field] for field in present_fields}

    if len({'', None}.intersection(values_fields)) > 0:
        return False

    return True


def modify_reponse(response_instance):
    response_instance.pop('_state', None)
    response_instance.pop('password', None)
    response_instance.pop('is_superuser', None)
    response_instance.pop('is_staff', None)
    response_instance.pop('is_active', None)
    response_instance.pop('backend', None)
    return response_instance
