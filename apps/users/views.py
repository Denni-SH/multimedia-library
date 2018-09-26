from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .heplers import validate_mandatory_fields, modify_reponse
from .models import User
from .serializers import UserCreateSerializer, UserLoginSerializer
from rest_framework_jwt.views import ObtainJSONWebToken
from multilibrary.helpers import generate_response

class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            mandatory_fields = {'password', 'first_name', 'last_name', 'email'}
            validation_status, validation_result = validate_mandatory_fields(request.data, fields=mandatory_fields)
            if validation_status:
                user = self.create(request, *args, **kwargs)
                response_data = generate_response(status=True, payload={"user": user.data})
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                response_data = generate_response(status=False, payload={"message": validation_result})
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            response_data = generate_response(status=False, payload={"message": error.__dict__['detail']})
            return Response(response_data, status=error.__dict__.get('status'))


class UserLoginView(ObtainJSONWebToken):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            if user and token:
                user_instance = UserLoginSerializer(user).instance.__dict__
                user_instance = modify_reponse(user_instance)
                response_status = status.HTTP_200_OK
                payload = {'token': token,
                           'user': user_instance}
                response_data = generate_response(status=True, payload=payload)
            else:
                response_status = status.HTTP_401_UNAUTHORIZED
                payload = {'message':serializer.object.get('message')}
                response_data = generate_response(status=False, payload=payload)
        else:
            response_status = status.HTTP_400_BAD_REQUEST
            payload = {'message': 'Mandatory fields are missed!'}
            response_data = generate_response(status=False, payload=payload)
        return Response(response_data, status=response_status)
