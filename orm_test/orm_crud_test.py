# from models import *
#
#
# # 参考代码，需要在django环境下执行，不能单独执行该文件
#
# # 插入数据
# user = User.objects.create(username='lisi', age=21, phone='13122432673', email='lisi@163.com')
# from orm_test.models import *
# # 查询数据
# xiaoming = User.objects.get(pk=1)
# # 获取该实例的关联对象
# xiaoming.profile
# xiaoming.groups
#
# # 查询多对多关联：xiaoming所在的全部组
# xiaohua = User.objects.get(pk=2)
# groups = xiaohua.groups
# groups.values()
# groups.values('name')
#
# # 聚合函数
# from django.db.models import *
# User.objects.aggregate(Avg('age'))
