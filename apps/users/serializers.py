from rest_framework.serializers import Serializer

from apps.users.user_helpers import modify_reponse
from .models import User
from calendar import timegm
from datetime import datetime
from multilibrary import settings


class UserSerializer(Serializer):
    class Meta:
        model = User
        fields = '__all__'
        # fields = ['id', 'username', 'first_name', 'last_name', 'email', 'avatar', 'birth_date', 'phone', 'thumbnail']


def jwt_response_payload_handler(token, user=None, request=None):
    """ Custom response payload handler.

    This function controlls the custom payload after login or token refresh. This data is returned through the web API.
    """
    response_instance = UserSerializer(user).instance.__dict__
    response_instance = modify_reponse(response_instance)
    return {
        'token': token,
        'user': response_instance
    }
