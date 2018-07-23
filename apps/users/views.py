from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    print(request.user.username)
    return HttpResponse('hello_world! %s' %request)

