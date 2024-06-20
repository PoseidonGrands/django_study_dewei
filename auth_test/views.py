from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import *
from django.contrib.auth.hashers import *
from django.contrib.auth.decorators import *
from django.contrib.auth import *
from django.http import *


#
#
# """对用户权限管理的demo"""
#
# def auth_reg(request):
#     if request.method == 'GET':
#         # 判断当前是否已经登录
#         if request.user.is_authenticated:
#             print('当前已经登录')
#         error = request.GET.get('error')
#         return render(request, 'auth_reg.html', {'error': error})
#     else:
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         check_password = request.POST.get('check_password', '')
#
#         # if User.objects.filter(username=username).exists():
#         #     return redirect('/auth_test/auth_reg?error=用户名已经存在')
#
#         if password != check_password:
#             return redirect('/auth_test/auth_reg?error=两次输入密码不相同')
#
#         # 使用create方法创建用户的时候才需要手动加密
#         # hash_password = make_password(password)
#         user = User.objects.create_user(username=username, password=password)
#         return redirect(reverse('auth_login'))
#
#
# def auth_login(request):
#     if request.method == 'GET':
#         error = request.GET.get('error')
#         return render(request, 'auth_login.html',{'error': error})
#     else:
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         print(username, password)
#
#         # 检查当前用户是否已经过验证登录
#         user = authenticate(username=username, password=password)
#         if user:
#             print('登录成功')
#             # 将该用户信息注册进request中
#             login(request, user)
#         else:
#             print('登录失败')
#             return redirect('/auth_test/auth_login?error=登录失败，用户名或密码错误')
#
#         return render(request, 'auth_login.html')
#
#
# def auth_logout(request):
#     logout(request)
#     return render(request, 'auth_login.html')
#
#
# # @login_required(login_url='/auth_test/auth_login')    相当于：user = authenticate(username=username, password=password)
# # @permission_required(perm='look_a_page')              相当于：permission = Permission.objects.get(codename='look_a_page')
# def a(request):
#     # if request.method == 'GET':
#     # error = request.GET.get('error')
#
#     # 查看当前用户的权限
#     print(f'当前用户的权限是：{request.user.user_permissions.values()}')
#
#     # 检查当前用户是否有这个权限
#     if not request.user.has_perm('auth_test.look_a_page'):
#         print('当前没有权限')
#         raise Http404()
#         # return render(request, 'a.html', {'error': '你没有权限访问该页面'})
#
#     return render(request, 'a.html')
#
#
# def add_auth(request):
#     """a页面的权限：直接为某个用户添加某个权限"""
#     permission = Permission.objects.get(codename='look_a_page')
#     # 为当前登录的用户添加权限
#     user = request.user
#     # 添加权限
#     user.user_permissions.add(permission)
#     print(f'当前用户的权限是：{user.user_permissions.values()}')
#     # 更新会话
#     update_session_auth_hash(request, user)
#     return render(request, 'add_auth.html')
#
#
# def add_auth_by_group(request):
#     """b页面的权限：通过创建组，定义组的权限，然后将用户加入组，使得用户获得权限"""
#     user = request.user
#     group_b = Group.objects.filter(name='b').first()
#     if not group_b:
#         group_b = Group.objects.create(name='b')
#     # 将b_page的全部权限添加到group_b组中
#     permissions = Permission.objects.filter(content_type_id=20)
#     # print(permissions)
#     for perm in permissions:
#         print(perm)
#         group_b.permissions.add(perm)
#
#     # 查看b组的权限
#     # print(group_b)
#
#     # 将user加入group_b
#     user.groups.add(group_b)
#
#     return render(request, 'add_auth_by_group.html')
#
#
# def b(request):
#     user = request.user
#     print(f'当前用户是：{user.username}')
#     print(f'当前用户的权限是：{user.user_permissions.values()}')
#
#     # 拿出查看b页面的权限
#     perm_look_b = Permission.objects.filter(codename='look_b_page').first()
#     # 检查哪些用户有查看b页面的权限（个人权限或组权限
#     users = User.objects.filter(Q(groups__permissions=perm_look_b) | Q(user_permissions=perm_look_b)).distinct()
#     print(f'有查看b页面权限的用户:{users}')
#     print(user)
#     if user not in users:
#         raise Http404()
#
#     return render(request, 'b.html')


def auth_reg(request):
    if request.method == 'GET':
        error = request.GET.get('error')
        return render(request, 'auth_reg.html', {'error': error})
    else:
        username = request.POST.get('username', '')
        pwd = request.POST.get('password', '')
        check_pwd = request.POST.get('check_password', '')

        # 是否存在用户
        user = User.objects.filter(username=username).exists()
        if user:
            return redirect('/auth_test/auth_reg?error=用户已存在')

        # 密码相同
        if pwd != check_pwd:
            return redirect('/auth_test/auth_reg?error=两次输入的密码不一致')

        # 创建用户
        user = User.objects.create_user(username=username, password=pwd)

        return redirect(reverse('auth_login'))


def auth_login(request):
    if request.method == 'GET':
        error = request.GET.get('error')
        return render(request, 'auth_login.html', {'error': error})
    else:
        username = request.POST.get('username')
        pwd = request.POST.get('password')

        user = authenticate(username=username, password=pwd)
        # 验证通过
        if user:
            login(request, user)
            return redirect(reverse('auth_login'))

        else:
            return redirect('/auth_test/auth_login?error=用户名或密码不正确')


def auth_logout(request):
    logout(request)
    return render(request, 'auth_login.html')


def a(request):
    """进入该页面需要用户已登录并且有该页面的权限"""

    error = request.GET.get('error')
    # 有错误信息
    if error:
        return render(request, 'a.html', {'error': error})

    print(User.objects.all())
    print(f'当前用户是：{request.user}')
    print(f'当前用户的权限是：{request.user.user_permissions.values()}')
    # 获取当前登录的用户
    _user = request.user
    # 获取全部用户
    all_user = User.objects.all()
    # 当前登录的用户是否在用户列表中
    if _user not in all_user:
        return redirect('/auth_test/a?error=您需要登录')

    # 检查用户是否有该页面需要的访问权限
    if not _user.has_perm('auth_test.look_a_page'):
        return redirect('/auth_test/a?error=您没有权限访问该页面')

    return render(request, 'a.html')


def b(request):
    error = request.GET.get('error')
    if error:
        return render(request, 'b.html', {'error': error})

    # 检查用户是否登录以及是否有查看该页面的权限
    _user = request.user
    user_all = User.objects.all()
    if _user not in user_all:
        return redirect('/auth_test/b?error=用户没有登录')

    # 权限要求
    perm_look_b_page = Permission.objects.filter(codename='look_b_page').first()
    if perm_look_b_page:
        users = User.objects.filter(Q(groups__permissions=perm_look_b_page)
                                   | Q(user_permissions=perm_look_b_page)).distinct()
        print(f'有查看b页面权限的用户:{users}')
        # 当前用户是否在有权限的用户列表中
        if _user not in users:
            return redirect('/auth_test/b?error=当前用户没有权限访问该页面')
    else:
        return redirect('/auth_test/b?error=页面的访问权限没有定义')

    return render(request, 'b.html')


def add_auth(request):
    _user = request.user
    perm = Permission.objects.get(codename='look_a_page')
    _user.user_permissions.add(perm)
    # 刷新会话
    update_session_auth_hash(request, _user)
    return render(request, 'add_auth.html')


def add_auth_by_group(request):
    # 检查组是否存在
    b_group = Group.objects.filter(name='b_group').first()
    if not b_group:
        b_group = Group.objects.create(name='b_group')
    perms = Permission.objects.filter(content_type_id=20)
    # 添加组权限
    for perm in perms:
        b_group.permissions.add(perm)

    # print(b_group.permissions)

    # 将用户加入该组
    _user = request.user
    _user.groups.add(b_group)

    return render(request, 'add_auth_by_group.html')
