from .views import UserCreateView, UserLoginView
from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    path('registration/', UserCreateView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('refresh_token/', refresh_jwt_token, name='refresh_token'),
]
