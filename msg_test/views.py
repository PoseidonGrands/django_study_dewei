
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .forms import *
from django.contrib.auth import *
from django.contrib.auth.decorators import *

from msg_test.consts import MessageType

"""
关于消息的练习
版本1：通过两种方式或两种方式结合获取消息
版本2：一个页面创建消息（通过传递参数）并保存到数据库，一个页面从数据库获取消息，并能通过在页面传递search参数进行模糊搜索
版本3：一个页面创建消息（通过表单提交）并保存到数据库，一个页面从数据库获取消息，并能通过在页面传递search参数进行模糊搜索
版本4：注册登录，加上获取消息页面的权限控制（作业：把每条消息的userid加上
"""


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


@login_required
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

        Message.objects.create(user=request.user, content=msg, msg_type=msg_type.value[0], create_time=time.time())

        return redirect(reverse('get_msg_data_2'))


@login_required(login_url='/msg_test/user_login')
@permission_required(perm='msg_test.view_message')
def get_msg_data_2(request):
    # # if not request.user.has_perm('msg_test.view_message'):
    #     print('当前没有权限')

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


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        # 前端已经用bootstrap展示信息了，所以这里只需要用表单将前端提交的信息验证即可
        form = RegisterForm(request.POST)
        if not form.is_valid():
            errors = form.non_field_errors()
            return render(request, 'register.html', {'errors': errors})
        else:
            return redirect('/msg_test/user_login')


def user_login(request):
    if request.method == 'GET':
        # login_required校验不通过跳转到当前页面时获取next参数
        next_return = request.GET.get('next')
        print(next_return)
        return render(request, 'login.html')
    else:
        # 前端已经用bootstrap展示信息了，所以这里只需要用表单将前端提交的信息验证即可
        form = LoginForm(request.POST)
        if not form.is_valid():
            print('验证不成功')
            errors = form.non_field_errors()
            return render(request, 'login.html', {'errors': errors})
        else:
            user = form.cleaned_data['user']
            if user:
                login(request, user)
            print('登录成功')
            return redirect('/msg_test/create_msg_data_2')


def user_logout(request):
    logout(request)
    return redirect('/msg_test/user_login')


def add_auth_get_msg(request):
    _user = request.user
    perm = Permission.objects.get(codename='view_message')
    if perm:
        print(f'添加权限:{perm}')
        _user.user_permissions.add(perm)
    print(_user.user_permissions)
    update_session_auth_hash(request, _user)
    return render(request, 'add_auth_get_msg.html')