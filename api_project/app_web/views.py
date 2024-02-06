import json

from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse


# Create your views here.

# post请求
def login(request):
    try:
        data = json.loads(request.body)
        if "name" in data and "password" in data:
            if data["name"] == "admin123" and data["password"] == "111111":
                return JsonResponse(dict(code=1, msg="ok"))
        return JsonResponse(dict(code=0, msg="fail"))
    except Exception as e:
        return JsonResponse(dict(code=0, msg=f"{e}"))
