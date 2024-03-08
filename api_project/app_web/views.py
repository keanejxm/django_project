import json
from app_web.yuxin_tiecheng.data_web import DataWeb
from django.views import View
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


def table_list(request):
    try:
        data = [{
            "date": '2016-05-02',
            "name": '王小虎',
            "address": '上海市普陀区金沙江路 1518 弄',
            "tag": '家'
        }, {
            "date": '2016-05-04',
            "name": '王小虎',
            "address": '上海市普陀区金沙江路 1517 弄',
            "tag": '公司'
        }, {
            "date": '2016-05-01',
            "name": '王小虎',
            "address": '上海市普陀区金沙江路 1519 弄',
            "tag": '家'
        }, {
            "date": '2016-05-03',
            "name": '王小虎',
            "address": '上海市普陀区金沙江路 1516 弄',
            "tag": '公司'
        }]

        return JsonResponse(dict(code=1, msg="ok", result=data))
    except Exception as e:
        return JsonResponse(dict(code=0, msg="fail", reason=e))


def wms_list(request):
    try:
        data = [
            {
                "id": "1",
                "title": "一致性 Consistency",
                "content": [
                    "与现实生活一致：与现实生活的流程、逻辑保持一致，遵循用户习惯的语言和概念；",
                    "在界面中一致：所有的元素和结构需保持一致，比如：设计样式、图标和文本、元素的位置等。"
                ]
            },
            {
                "id": "2",
                "title": "反馈 Feedback",
                "content": [
                    "控制反馈：通过界面样式和交互动效让用户可以清晰的感知自己的操作；",
                    "页面反馈：操作后，通过页面元素的变化清晰地展现当前状态。"
                ]
            },
            {
                "id": "3",
                "title": "效率 Efficiency",
                "content": [
                    "简化流程：设计简洁直观的操作流程",
                    "清晰明确：语言表达清晰且表意明确，让用户快速理解进而作出决策；",
                    "帮助用户识别：界面简单直白，让用户快速识别而非回忆，减少用户记忆负担。"
                ]
            },
            {
                "id": "4",
                "title": "可控 Controllability",
                "content": [
                    "用户决策：根据场景可给予用户操作建议或安全提示，但不能代替用户进行决策；",
                    "结果可控：用户可以自由的进行操作，包括撤销、回退和终止当前操作等。"
                ]
            },
        ]
        return JsonResponse(dict(code=1, msg="ok", result=data))
    except Exception as e:
        return JsonResponse(dict(code=0, msg="fail", reason=e))


# class YuXinTieCheng(View):
#     def __init__(self):
#         super().__init__()
#         self.data_web = DataWeb()
#
#     def get(self, request):
#         pass
#
#     def status_count(self, request):
#         def get(request):
#             data = self.data_web.count_task_status()
#             return JsonResponse(dict(code=1, msg="ok", data=data))

def yu_xin_status_count(request):
    data_web = DataWeb()
    data = data_web.count_task_status()
    return JsonResponse(dict(code=1, msg="ok", data=data))
