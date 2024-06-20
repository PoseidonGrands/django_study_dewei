from django.contrib import admin
from django.utils.html import format_html

from .models import *


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """这里调用注册的model里的变量或函数"""
    list_display = ['id', 'content', 'msg_type', 'convert_time', 'redirect']
    # 设置只读属性，无法在后台修改
    readonly_fields = ('msg_type', 'create_time')

    # 设置右边过滤项目，可根据msg_type的分类值进行筛选
    list_filter = ('msg_type', )

    # 提供搜索栏，针对哪个字段进行搜索
    search_fields = ['content']        # 针对content的内容进行搜索（可模糊搜索

    ordering = ['id']   # 根据id进行排序

    list_per_page = 4   # 每页展示的数据

    # 在后台中修改或创建数据时触发
    def save_model(self, request, obj, form, change):
        if change:
            obj.content = obj.content + 'update'
        else:
            obj.content = obj.content + 'create'
        super(MessageAdmin, self).save_model(request, obj, form, change)

    def redirect(self, obj):
        return format_html('<a href="{}">跳转</a>', 'https://www.baidu.com')