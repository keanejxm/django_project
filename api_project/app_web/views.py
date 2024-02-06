from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse


# Create your views here.

def login(request):
    return JsonResponse(dict(code=0, msg="成功"))
