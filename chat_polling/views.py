from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json

# 简易数据库，存放消息
DB = []


def poll(request):
    return render(request, 'poll.htm')


def send_msg(request):
    print("接收到客户端请求：", request.GET)
    text = request.GET.get('text')
    DB.append(text)

    return HttpResponse("ok")


def get_msg(request):
    index = request.GET.get('index')
    index = int(index)
    context = {
        "data": DB[index:],
        "max_index": len(DB)
    }

    return JsonResponse(context)
