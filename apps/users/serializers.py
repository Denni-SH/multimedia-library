from rest_framework.compat import authenticate
from rest_framework.serializers import ModelSerializer
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler

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


class UserLoginSerializer(JSONWebTokenSerializer):

    username_field = 'login'

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'avatar', 'birth_date', 'phone', 'thumbnail']
        extra_kwargs = {"password": {"write_only": True},
                        "_state": {"write_only": True},
                        "is_superuser": {"write_only": True},
                        "is_staff": {"write_only": True},
                        "is_active": {"write_only": True},
                        "backend": {"write_only": True},
                        }

    def validate(self, attrs):

        password = attrs.get("password")
        user_obj = User.objects.filter(email=attrs.get("login")).first() or User.objects.filter(
            username=attrs.get("login")).first()
        if user_obj is not None:
            credentials = {
                'username': user_obj.username,
                'password': password
            }
            if all(credentials.values()):
                authenticated_user = authenticate(**credentials)
                if authenticated_user:
                    if not authenticated_user.is_active:
                        msg = 'User account is disabled.'
                        return {'message': msg}

                    payload = jwt_payload_handler(authenticated_user)

                    return {
                        'token': jwt_encode_handler(payload),
                        'user': authenticated_user
                    }
                else:
                    msg = 'Unable to log in with provided credentials.'
                    return {'message': msg}

            else:
                msg = 'Must include "{username_field}" and "password".'
                msg = msg.format(username_field=self.username_field)
                return {'message': msg}

        else:
            msg = 'Account with this email/username does not exists'
            return {'message': msg}


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'avatar', 'birth_date', 'phone', 'thumbnail']
        extra_kwargs = {"password": {"write_only": True},
                        "_state": {"write_only": True},
                        "is_superuser": {"write_only": True},
                        "is_staff": {"write_only": True},
                        "is_active": {"write_only": True},
                        "backend": {"write_only": True},
                        }
