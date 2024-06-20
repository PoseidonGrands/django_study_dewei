import time

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .forms import *

from msg_test.consts import MessageType


def get_msg_1(request):
    """通过request获取url参数"""
    msg = request.GET.get('msg', '空消息')
    return render(request, 'index.html', {
        'msg': msg
    })


def get_msg_2(request, msg):
    """通过url获取参数/xx/参数"""
    if msg is None:
        msg = '空消息'
    return render(request, 'index.html', {
        'msg': msg
    })


def get_msg_3(request, msg_type):
    """1和2结合"""
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


def create_msg_data(request, msg_type):
    template_file = 'create_msg_data.html'
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

    # 保存到数据库
    Message.objects.create(content=msg, msg_type=msg_obj.value[0], create_time=time.time())

    return redirect(reverse('get_msg_data'))


def get_msg_data(request):
    template_file = 'get_msg_data.html'

    # 搜索条件
    search = request.GET.get('search', '')
    # 从数据库读取消息
    print(search)
    if search:
        msgs = Message.objects.filter(content__contains=search)
    else:
        msgs = Message.objects.all()

    return render(request, template_file,
                  {
                      'msgs': msgs
                  })

def create_msg_data_2(request):
    template_file = 'create_msg_data_2.html'

    if request.method == 'GET':
        return render(request, template_file, {
            'form': MessageForm
        })
    else:
        # 表单验证
        form = MessageForm(request.POST)
        if not form.is_valid():
            return render(request, template_file, {
                # ！！！！！注意：应该传递表单实例 form 到模板中，而不是重新创建一个新的表单实例 MessageForm
                # 'form': MessageForm   这种方式是错的
                'form': form
            })
        msg = form.cleaned_data.get('message')
        msg_type = form.cleaned_data.get('message_type')

        Message.objects.create(content=msg, msg_type=msg_type.value[0], create_time=time.time())

        return redirect(reverse('get_msg_data_2'))


def get_msg_data_2(request):
    template_file = 'get_msg_data_2.html'

    # 搜索条件
    search = request.GET.get('search', '')
    # 从数据库读取消息
    print(search)
    if search:
        msgs = Message.objects.filter(content__contains=search)
    else:
        msgs = Message.objects.all()

    return render(request, template_file,
                  {
                      'msgs': msgs
                  })