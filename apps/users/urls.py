from .views import UserCreateView, UserLoginView, UserVerifyView, UserRetrieveUpdateDestroyView, UserListView
from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    path('auth/registration', UserCreateView.as_view(), name='register'),
    path('auth/login', UserLoginView.as_view(), name='login'),
    path('auth/refresh_token', refresh_jwt_token, name='refresh_token'),
    path('auth/verify/<uuid:uuid>', UserVerifyView.as_view(), name='verify_post'),

    path('get_or_update_user_info/id=<pk>', UserRetrieveUpdateDestroyView.as_view(), name='get_or_update_user_info'),
    path('delete_user', UserRetrieveUpdateDestroyView.as_view(), name='delete_user'),
    path('upload_image', UserRetrieveUpdateDestroyView.as_view(), name='upload_image'),
    path('get_user_list', UserListView.as_view(), name='get_user_list'),
]