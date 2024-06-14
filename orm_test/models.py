from django.db import models

# Create your models here.
class Test(models.Model):
    username = models.CharField('username', max_length=64, unique=True)
    age = models.PositiveIntegerField('年龄')


# 区分
# blank为True，null为True，表单不输入存储null
# blank为True，null为True，设置default，表单不输入存储默认值，但是可以存储Null值
class User(models.Model):
    # 自定义的id不会自增
    # id = models.IntegerField(primary_key=True)
    username = models.CharField('用户名', max_length=64)
    age = models.SmallIntegerField('年龄', default=0, blank=True)
    phone = models.CharField('手机号码', max_length=20, db_index=True, default='', blank=True)
    email = models.CharField('邮箱', default='', blank=True, max_length=128)
    info = models.TextField('个人描述', default='', blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        index_together = ['username', 'phone']

    def __str__(self):
        return f'User:{self.username}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birthday = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'UserProfile:{self.user.username}-{self.birthday}'


class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diarys')
    content = models.TextField()


class Group(models.Model):
    name = models.CharField(max_length=64)
    user = models.ManyToManyField(User, related_name='groups')
