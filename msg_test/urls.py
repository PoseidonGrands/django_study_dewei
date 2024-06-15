from django.urls import path
from msg_test.views import *

urlpatterns = [
    path('get_msg_1', get_msg_1, name='get_msg_1'),
    path('get_msg_2/<str:msg>', get_msg_2, name='get_msg_2'),
    path('get_msg_3/<str:msg_type>', get_msg_3, name='get_msg_3'),
    path('create_msg_data/<str:msg_type>', create_msg_data, name='create_msg_data'),
    path('get_msg_data', get_msg_data, name='get_msg_data')
]

