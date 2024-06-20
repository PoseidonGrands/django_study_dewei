import jieba
from django import forms
from django.contrib.auth.models import *
from django.contrib.auth import authenticate
from .consts import *

# 动态载入消息类型
MessageTypeChoice = tuple([(message.value[0], message.value[0]) for message in MessageType])


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # 判断用户名、密码是否已填写
        if not username:
            raise forms.ValidationError('用户名未填写')
        if not password:
            raise forms.ValidationError('密码未填写')

        # 数据库是否存在该用户
        users = User.objects.filter(username=username).exists()
        if not users:
            print('用户不存在')
            raise forms.ValidationError('用户不存在')

        user = authenticate(username=username, password=password)
        if not user:
            print('密码不正确')
            raise forms.ValidationError('密码不正确')

        # 将用户保存
        self.cleaned_data['user'] = user

        return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    check_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        check_password = self.cleaned_data.get('check_password')
        # 判断用户名、密码、确认密码是否已填写
        if not username:
            raise forms.ValidationError('用户名未填写')
        if not password:
            raise forms.ValidationError('密码未填写')
        if not check_password:
            raise forms.ValidationError('确认密码未填写')
        if password != check_password:
            raise forms.ValidationError('两次输入的密码不一致')

        # 数据库检查是否有该用户
        user = User.objects.filter(username=username).exists()
        if user:
            raise forms.ValidationError('该用户已经注册')

        # 创建用户
        User.objects.create_user(username=username, password=password)

        return self.cleaned_data


class MessageForm(forms.Form):
    message = forms.CharField(label='消息内容', max_length=256)
    # message_type = forms.CharField(label='消息类型', max_length=10)
    message_type = forms.CharField(label='消息类型', max_length=10, widget=forms.Select(choices=MessageTypeChoice))

    def clean_message(self):
        msg = self.cleaned_data.get('message', '')
        if not msg:
            raise forms.ValidationError('消息不能为空')

        cuts = jieba.lcut(msg)
        # 检查是否有一级违禁词
        check = list(set(cuts) & set(SENSITIVE_WORDS_DANGER))
        if check:
            raise forms.ValidationError('存在敏感词汇，消息已被屏蔽')
        return msg

    def clean_message_type(self):
        # 不能为空
        msg_type = self.cleaned_data.get('message_type')
        if not msg_type:
            raise forms.ValidationError('消息类型不能为空')
        # 检查消息类型是否存在
        try:
            # msg_type_obj = MessageType['a']
            msg_type_obj = MessageType[msg_type]
        except Exception as e:
            raise forms.ValidationError('该消息类型不存在')
        return msg_type_obj
