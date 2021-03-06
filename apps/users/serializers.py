import copy
from rest_framework.compat import authenticate
from rest_framework.relations import RelatedField
from rest_framework.serializers import ModelSerializer, CharField
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler

from .models import User

USER_EXTRA_KWARGS = dict.fromkeys(['_state',
                                   'is_superuser',
                                   'is_staff',
                                   'password',
                                   'is_active',
                                   'backend'
                                   ], {"write_only": True})
USER_EXTRA_KWARGS.update(dict.fromkeys(['email',
                                        'thumbnail'
                                        ], {"read_only": True}))


USER_FIELDS = ['id',
               'username',
               'first_name',
               'last_name',
               'email',
               'avatar',
               'birth_date',
               'phone',
               'thumbnail']


class UserSerializer(ModelSerializer):
    avatar = CharField(max_length=None)
    thumbnail = CharField(max_length=None)
    # files = RelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = USER_FIELDS
        extra_kwargs = copy.deepcopy(USER_EXTRA_KWARGS)


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = copy.deepcopy(USER_FIELDS)
        fields.append('password')
        extra_kwargs = copy.deepcopy(USER_EXTRA_KWARGS)
        extra_kwargs['email']['read_only'] = False

    def create(self, request, *args, **kwargs):
        user = User.create(**request)
        user.save()
        return user


class UserLoginSerializer(JSONWebTokenSerializer):

    username_field = 'login'

    class Meta(UserSerializer.Meta):
        model = User
        fields = USER_FIELDS
        extra_kwargs = USER_EXTRA_KWARGS

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
