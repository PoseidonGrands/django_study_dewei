from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from msg_test.consts import MessageType


# Create your views here.
def get_msg_1(request):
    msg = request.GET.get('msg', '空消息')
    return render(request, 'index.html', {
        'msg': msg
    })


def get_msg_2(request, msg):
    if msg is None:
        msg = '空消息'
    return render(request, 'index.html', {
        'msg': msg
    })


def get_msg_3(request, msg_type):
    template_file = 'msg_type.html'
    # 验证消息类型是否存在
    data = {}
    try:
        msg_obj = MessageType[msg_type]
    except Exception as e:
        data['error'] = f'没有这个消息类型:{e}'
        return render(request, template_file, data)

    # 消息是否为空
    msg = request.GET.get('msg', '')
    if msg is None:
        data['error'] = f'消息不能为空'
        return render(request, template_file, data)

    # 传递消息和消息类型数据
    data['msg'] = msg
    data['msg_obj'] = msg_obj
    print(msg_obj.color)
    return render(request, template_file, data)
