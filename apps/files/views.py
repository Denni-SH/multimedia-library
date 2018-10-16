import json
from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import OrderingFilter

from multilibrary.helpers import generate_formatted_response
from multilibrary.settings import MEDIA_ROOT, FILE_MAX_SIZE, FILE_MAX_SIZE_NUMBER

from apps.users.permissions import IsVerified, HasPermissionOrReadOnly

from .filters import FileFilter
from .helpers import is_exist_or_save_file
from .models import UserFile
from .pagination import FilePageNumberPagination
from .serializers import FileSerializer


class FileListView(ListAPIView):
    queryset = UserFile.objects.all()
    serializer_class = FileSerializer
    permission_classes = (IsAuthenticated, IsVerified)
    pagination_class = FilePageNumberPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filter_class = FileFilter
    ordering = ['-timestamp']


class FileRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsVerified, HasPermissionOrReadOnly)
    serializer_class = FileSerializer

    def get_object(self, file_pk=None):
        obj = UserFile.objects.get(pk=file_pk)
        self.check_object_permissions(self.request, obj.owner)
        return obj

    def delete(self, request, *args, **kwargs):
        try:
            file_pk = int(kwargs['pk'])
            if file_pk:
                file_instance = UserFile.objects.filter(pk=file_pk)
                if file_instance and self.get_object(file_pk):
                    file_instance.delete()
                    response_status = status.HTTP_200_OK
                    response_data = generate_formatted_response(status=True, payload={'message': 'Success removed!'})
            else:
                raise Exception()
        except Exception as error:
            if error.args and error.args[0].get('message'):
                payload = error.args[0].get('message')
            elif hasattr(error, 'detail'):
                payload = error.detail
            else:
                payload = "Bad response!"

            if error.args and error.args[0].get('status'):
                response_status = error.args[0].get('status')
            elif error.args and error.args[0].get('status_code'):
                response_status = error.args[0].get('status_code')
            elif hasattr(error, 'status_code'):
                response_status = error.status_code
            else:
                response_status = status.HTTP_400_BAD_REQUEST
            response_data = generate_formatted_response(status=False, payload={'message': payload})
        return Response(response_data, status=response_status)


class FileCreateView(CreateAPIView):
    queryset = UserFile.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated, IsVerified]
    parser_classes=(MultiPartParser, )

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            request_data = eval(json.dumps(request.POST))
            new_file = request.data.get('file')
            if new_file and new_file.size <= FILE_MAX_SIZE:
                filename, ext = str(new_file).rsplit(".", 1)
                title = request_data.get('title', filename)
                user_files = [item.title for item in user.files.all()]
                if title not in user_files:
                    filename += f'_{datetime.now().timestamp()}'
                    file_rel_path = f'{user.pk}/{filename}.{ext}'
                    file_abs_path = f'{MEDIA_ROOT}/{file_rel_path}'
                    request_data['file'] = file_rel_path
                    request_data['owner'] = request.user.pk

                    is_exist_or_save_file(user.pk, file_abs_path, new_file)

                    serializer = self.serializer_class(data=request_data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                    response_status = status.HTTP_200_OK
                    response_data = generate_formatted_response(status=True, payload={'file': serializer.data})
                else:
                    raise Exception({'message': "You have the file with this title already! Rename it please."})
            else:
                raise Exception({'message': f"Please import file with size smaller than {FILE_MAX_SIZE_NUMBER} GB!"})
        except Exception as error:
                print(f'{type(error)}:{error.detail}') if hasattr(error, 'detail') else f'{type(error)}'
                payload = error.args[0].get('message') \
                    if error.args and hasattr(error.args[0], 'get') and error.args[0].get('message') \
                    else "Bad request!"
                response_status = status.HTTP_400_BAD_REQUEST
                response_data = generate_formatted_response(status=False, payload={'message': payload})
        return Response(response_data, status=response_status)