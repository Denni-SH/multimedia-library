import base64
import os

from django.db.models.base import ObjectDoesNotExist
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework_jwt.views import ObtainJSONWebToken

from multilibrary.helpers import generate_formatted_response
from multilibrary.settings import MEDIA_ROOT

from .heplers import validate_mandatory_fields, modify_user_reponse
from .models import User
from .serializers import UserLoginSerializer, UserSerializer, UserCreateSerializer
from .pagination import UserPageNumberPagination
from .permissions import HasPermissionOrReadOnly, IsVerified


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
                response_data = generate_formatted_response(status=True, payload={"user": user.data})
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                response_data = generate_formatted_response(status=False, payload={"message": validation_result})
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            response_data = generate_formatted_response(status=False, payload={"message": str(type(error))})
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
                user_instance = modify_user_reponse(UserLoginSerializer(user).instance.__dict__)
                response_status = status.HTTP_200_OK
                payload = {'user': user_instance,
                           'token': token}
                response_data = generate_formatted_response(status=True, payload=payload)
            else:
                response_status = status.HTTP_401_UNAUTHORIZED
                payload = {'message': serializer.object.get('message')}
                response_data = generate_formatted_response(status=False, payload=payload)
        else:
            response_status = status.HTTP_400_BAD_REQUEST
            payload = {'message': 'Mandatory fields are missed!'}
            response_data = generate_formatted_response(status=False, payload=payload)
        return Response(response_data, status=response_status)


class UserVerifyView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def get(request, uuid):
        try:
            user = User.objects.get(verification_uuid=uuid, is_verified=False)
        except User.DoesNotExist:
            payload = {'message': "User does not exist or is already verified"}
            response_status = status.HTTP_404_NOT_FOUND
            response_data = generate_formatted_response(status=False, payload=payload)
            return Response(response_data, status=response_status)
        else:
            user.is_verified = True
            user.save()
            response_status = status.HTTP_200_OK
            response_data = generate_formatted_response(status=True, payload={})

        return Response(response_data, status=response_status)


class UserUpdateView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, HasPermissionOrReadOnly, IsVerified)
    serializer_class = UserSerializer

    def get_object(self, user_pk=None):
        obj = User.objects.get(pk=user_pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        try:
            user_pk = int(kwargs['pk'])
            user_instance = self.get_object(user_pk)
        except (ObjectDoesNotExist, ValueError):
            response_status = status.HTTP_404_NOT_FOUND
            response_data = generate_formatted_response(status=False, payload={'message': "This user doesn't exists!"})
        else:
            serializer = self.serializer_class(user_instance)
            response_status = status.HTTP_200_OK
            response_data = generate_formatted_response(status=True, payload={'user': serializer.data})

        return Response(response_data, status=response_status)

    def put(self, request, *args, **kwargs):
        try:
            user_pk = request.user.pk
            user_instance = self.get_object(user_pk)
        except (ObjectDoesNotExist, ValueError):
            response_status = status.HTTP_404_NOT_FOUND
            response_data = generate_formatted_response(status=False, payload={'message': "This user doesn't exists!"})
        except PermissionDenied:
            raise PermissionDenied
        except Exception as error:
            print(f'{type(error)}:{error.detail}') if hasattr(error, 'detail') else f'{type(error)}'
            response_status = status.HTTP_400_BAD_REQUEST
            response_data = generate_formatted_response(status=False, payload={'message': "Bad response!"})
        else:
            serializer_data = request.data.get('user', {})
            serializer = UserSerializer(
                user_instance, data=serializer_data, partial=True
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()

            response_status = status.HTTP_200_OK
            response_data = generate_formatted_response(status=True, payload={'user': serializer.data})

        return Response(response_data, status=response_status)

    # def patch(self, request, *args, **kwargs):
    #
    #     try:
    #         user_pk = request.user.pk
    #         user_instance = self.get_object(user_pk)
    #         image = request.data.get('avatar', None)
    #         image_filename = request.data.get('filename', 'avatar.jpg')
    #         image_path = f'{MEDIA_ROOT}/{user_pk}'
    #         if not os.path.exists(image_path):
    #             os.makedirs(image_path)
    #         full_path = f'{image_path}/{image_filename}'
    #         print(full_path)
    #         with open(full_path, "w+b") as new_image:
    #             new_image.write(base64.urlsafe_b64decode(image.encode()))
    #         with open(full_path, "r") as few_image:
    #             few_image.read()
    #         serializer_data = {"avatar": new_image}
    #         serializer = UserSerializer(
    #             user_instance, data=serializer_data, partial=True
    #         )
    #
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #     except (ObjectDoesNotExist, ValueError) as error:
    #         print(type(error), error)
    #         response_status = status.HTTP_404_NOT_FOUND
    #         response_data = generate_formatted_response(status=False, payload={'message': "This user doesn't exists!"})
    #     except PermissionDenied:
    #         raise PermissionDenied
    #     except Exception as error:
    #         print(f'{type(error)}:{error.detail}') if hasattr(error, 'detail') else f'{type(error)}'
    #         response_status = status.HTTP_400_BAD_REQUEST
    #         response_data = generate_formatted_response(status=False, payload={'message': "Bad response!"})
    #     else:
    #         response_status = status.HTTP_200_OK
    #         response_data = generate_formatted_response(status=True, payload={'user': serializer.data})
    #
    #     return Response(response_data, status=response_status)


class UserListView(ListAPIView):
    pagination_class = UserPageNumberPagination
    permission_classes = (IsAuthenticated, IsVerified)
    queryset = User.objects.all()
    serializer_class = UserSerializer
