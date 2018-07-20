from django.http import HttpResponse
from django.shortcuts import render
# from rest_framework_jwt.authentication import

def hello(request):
    print(request.user.username)
    return HttpResponse('hello_world! %s' %request)

# example custom serializer for
def jwt_response_payload_handler(token, user=None, request=None):
    print('debug is missed(')
    import os
    print(os.environ)
    return {
        'token': token,
        'user': dict(user, context={'request': request})
    }