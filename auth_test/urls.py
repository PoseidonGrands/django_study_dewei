from django.urls import *
from .views import *

urlpatterns = [
    path('auth_reg', auth_reg, name='auth_reg'),
    path('auth_login', auth_login, name='auth_login'),
    path('auth_logout', auth_logout, name='auth_logout'),
    path('a', a, name='a'),
    path('b', b, name='b'),
    path('add_auth', add_auth, name='add_auth'),
    path('add_auth_by_group', add_auth_by_group, name='add_auth_by_group'),
]