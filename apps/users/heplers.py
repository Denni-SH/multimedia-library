import os
from multilibrary.settings import MEDIA_ROOT

from apps.users.models import User


def validate_mandatory_fields(data, fields=set()):
    """ Checks for missing/empty fields.
    """
    if not fields.issubset(set(data.keys())):
        return False, 'Mandatory fields are missed!'
    user = User.objects.filter(email=data['email'])
    if user:
        return False, 'This email is already exists!'
    # set username field to base django request validation
    elif not data.get('username'):
        data['username'] = f"{data['first_name'].lower()}_{data['last_name'].lower()}"

    return True, data


def modify_user_reponse(response_instance):
    del response_instance['_state'],\
        response_instance['password'],\
        response_instance['is_superuser'],\
        response_instance['is_staff'],\
        response_instance['is_active'],\
        response_instance['backend']
    return response_instance


def check_or_save_image(user_pk, avatar_filename, user_avatar):
    image_path = f'{MEDIA_ROOT}/{user_pk}'
    full_path = f'{image_path}/{avatar_filename}'

    if not os.path.exists(image_path):
        os.makedirs(image_path)
    with open(full_path, "wb") as new_image:
        for chunk in user_avatar.chunks():
            new_image.write(chunk)
