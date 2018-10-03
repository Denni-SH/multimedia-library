from .views import UserCreateView, UserLoginView, UserVerifyView, UserUpdateView
from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    path('auth/registration', UserCreateView.as_view(), name='register'),
    path('auth/login', UserLoginView.as_view(), name='login'),
    path('auth/refresh_token', refresh_jwt_token, name='refresh_token'),
    path('auth/verify/<uuid:uuid>', UserVerifyView.as_view(), name='verify_post'),
    path('get_or_update_user_info/id=<pk>', UserUpdateView.as_view(), name='get_or_update_user_info'),
    # path('upload_image', UserUpdateView.as_view(), name='upload_image'),
]