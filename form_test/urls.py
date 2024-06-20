from django.urls import path

from .views import *

urlpatterns = [
    path('reg', reg, name='reg'),
    path('login', login, name='login')
]