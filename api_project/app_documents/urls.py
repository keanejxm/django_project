from django.urls import path
from . import views

app_name = 'app_documents'

urlpatterns = [
    # API文档接口
    path('api/', views.APIDocumentationView.as_view(), name='api_docs'),
]