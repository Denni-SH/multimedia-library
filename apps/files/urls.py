from .views import FileListView, FileRetrieveUpdateDestroyView, FileCreateView
from django.urls import path


urlpatterns = [
    path('create_file', FileCreateView.as_view(), name='create_file'),
    path('get_files_list', FileListView.as_view(), name='get_files_list'),
    path('id=<pk>/delete', FileRetrieveUpdateDestroyView.as_view(), name='delete_file'),
    path('id=<pk>/update', FileRetrieveUpdateDestroyView.as_view(), name='update_file'),
    path('id=<pk>', FileRetrieveUpdateDestroyView.as_view(), name='get_file_info'),
]
