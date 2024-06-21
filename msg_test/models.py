import time

from django.db import models
from django.contrib.auth.models import User

from msg_test.consts import MessageType


class Message(models.Model):
    # 补充字段
    user = models.ForeignKey(User, null=True, default='', on_delete=models.SET_NULL, related_name='message')
    content = models.TextField()
    msg_type = models.CharField(max_length=32, db_index=True)
    create_time = models.IntegerField(default=0)

    def __str__(self):
        return f'type:{self.msg_type},content:{self.content}'

    @property
    def msg_obj(self):
        try:
            return MessageType[self.msg_type]
        except:
            return MessageType['info']

    def convert_time(self):
        _time = time.localtime(self.create_time)
        return time.strftime('%Y-%m-%d %H-%M-%S', _time)
