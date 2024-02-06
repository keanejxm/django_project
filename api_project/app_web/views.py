import json

from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse


# Create your views here.

# post请求
def login(request):
    try:
        data = json.loads(request.body)
        print(data)
        return HttpResponse("aaaaa")
    except Exception as e:
        return HttpResponse("bbbbbb")
