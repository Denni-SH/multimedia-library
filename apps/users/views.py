from datetime import datetime

from django.db.models.base import ObjectDoesNotExist
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework_jwt.views import ObtainJSONWebToken

from multilibrary.helpers import generate_formatted_response
from multilibrary.settings import MEDIA_ROOT, IMAGE_MAX_SIZE

from .heplers import validate_mandatory_fields, modify_user_reponse, is_exist_or_save_image
from .models import User
from .serializers import UserLoginSerializer, UserSerializer, UserCreateSerializer
from .tasks import save_thumbnail
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
            user_pk = int(kwargs['pk']) if kwargs.get('pk') else request.user.pk
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

    def patch(self, request, *args, **kwargs):
        try:
            user_pk = request.user.pk
            user_instance = self.get_object(user_pk)
            user_avatar = request.data.get('avatar', None)
            if user_avatar and user_avatar.size <= IMAGE_MAX_SIZE * 1024 * 1024:
                filename, ext = f'{datetime.now().timestamp()}', 'png'
                avatar_rel_path = f'{user_pk}/{filename}.{ext}'
                avatar_abs_path = f'{MEDIA_ROOT}/{avatar_rel_path}'
                thumb_rel_path = f'{user_pk}/{filename}_thumb.{ext}'
                thumb_abs_path = f'{MEDIA_ROOT}/{thumb_rel_path}'

                is_exist_or_save_image(user_pk, avatar_abs_path, user_avatar)
                save_thumbnail.delay(user_pk, thumb_abs_path, avatar_abs_path)
                serializer_data = {"avatar": avatar_rel_path,
                                   "thumbnail": thumb_rel_path}

                serializer = UserSerializer(
                    user_instance, data=serializer_data, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()

                user_data = serializer.data
            elif user_avatar.size > IMAGE_MAX_SIZE * 1024 * 1024:
                raise Exception({'message': "Image is bigger than 7 MB!"})
            else:
                user_data = UserSerializer(user_instance).data
            response_status = status.HTTP_200_OK
            response_data = generate_formatted_response(status=True, payload={'user': user_data})

        except (ObjectDoesNotExist, ValueError):
            response_status = status.HTTP_404_NOT_FOUND
            response_data = generate_formatted_response(status=False, payload={'message': "This user doesn't exists!"})
        except PermissionDenied:
            raise PermissionDenied
        except Exception as error:
            print(f'{type(error)}:{error.detail}') if hasattr(error, 'detail') else f'{type(error)}'
            payload = error.args[0].get('message') if error.args and error.args[0].get('message') else "Bad response!"
            response_status = status.HTTP_400_BAD_REQUEST
            response_data = generate_formatted_response(status=False, payload={'message': payload})
        return Response(response_data, status=response_status)


class UserListView(ListAPIView):
    pagination_class = UserPageNumberPagination
    permission_classes = (IsAuthenticated, IsVerified)
    queryset = User.objects.all()
    serializer_class = UserSerializer
