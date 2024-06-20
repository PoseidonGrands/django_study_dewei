from django import forms
from django.db import transaction
from django.forms import fields

from .models import *

class UserRegForm(forms.Form):
    username = fields.CharField(max_length=64)
    password = fields.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username', '')
        password = self.cleaned_data.get('password', '')
        if not username or not password:
            raise forms.ValidationError('用户名或密码不能为空')

        if len(username) > 10:
            raise forms.ValidationError('用户名长度不能大于10')


class UserRegModelForm(forms.ModelForm):
    class Meta:
        model = UserInfo

        fields = ['username', 'password']

        labels = {'username': '用户名', 'password': '密码'}

        widgets = {
            'password': forms.PasswordInput(
                attrs={'placeholder': '请输入密码'},
                # 控制密码字段在渲染时是否显示当前输入的值
                render_value=True
            )
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 8:
            raise forms.ValidationError('用户名不能大于8')
        return username
