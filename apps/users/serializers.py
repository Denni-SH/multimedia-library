from rest_framework.serializers import ModelSerializer, Serializer

from .heplers import modify_reponse
from .models import User


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'avatar', 'birth_date', 'phone', 'thumbnail', 'password']
        extra_kwargs = {"password":
                        {"write_only": True}
                        }

    def create(self, request, *args, **kwargs):
        user = User.create(**request)
        user.save()
        return user


class UserLoginSerializer(Serializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'avatar', 'birth_date', 'phone', 'thumbnail']


def jwt_response_payload_handler(token, user=None, request=None):
    """ Custom response payload handler.

    This function controlls the custom payload after login or token refresh. This data is returned through the web API.
    """
    response_instance = UserLoginSerializer(user).instance.__dict__
    response_instance = modify_reponse(response_instance)
    return {
        "is_successful": True,
        'token': token,
        'user': response_instance
    }
