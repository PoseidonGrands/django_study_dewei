import jieba
from django import forms
from .consts import *

# 动态载入消息类型
MessageTypeChoice = tuple([(message.value[0], message.value[0]) for message in MessageType])


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
