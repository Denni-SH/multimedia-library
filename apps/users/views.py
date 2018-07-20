import json
from calendar import timegm
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
# from rest_framework_jwt.authentication import
from multilibrary import settings
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = '__all__'


def hello(request):
    print(request.user.username)
    return HttpResponse('hello_world! %s' %request)

# example custom serializer for
def jwt_payload_handler(user):
    return {
        'user_id': user.pk,
        'email': user.email,
        'is_superuser': user.is_superuser,
        'exp': datetime.utcnow() + settings.JWT_AUTH['JWT_EXPIRATION_DELTA'],
        'orig_iat': timegm(
            datetime.utcnow().utctimetuple()
        )
    }

def jwt_response_payload_handler(token, user=None, request=None):
    """ Custom response payload handler.

    This function controlls the custom payload after login or token refresh. This data is returned through the web API.
    """
    response_instance = UserSerializer(user).data
    print(type(response_instance), response_instance)
    return {
        'token': token,
        'user': response_instance
    }
