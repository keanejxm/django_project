"""
URL configuration for api_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
import app_web.views as web_view

# from app_web.views import YuXinTieCheng

urlpatterns = [
    path("login/", web_view.login),
    path("tableList/", web_view.table_list),
    path("wmsList/", web_view.wms_list),
    # yuxin
    path("yuxin/status/count/", web_view.yu_xin_status_count),
    path("yuxin/person/count/", web_view.yu_xin_person_count),
    path("yuxin/module/count/", web_view.yu_xin_module_count),
    path("yuxin/date/use/story/", web_view.yu_xin_date_use_story),
    path("yuxin/schedule/story/", web_view.yu_xin_schedule_story),
    path("yuxin/flaw/story/count/", web_view.yu_xin_flaw_story_count),
    path("question/", web_view.yu_xin_flaw_story_count),

]
