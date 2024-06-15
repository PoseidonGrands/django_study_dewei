from django.db import models

from msg_test.consts import MessageType


class Message(models.Model):
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