# from django.conf.urls import url
from internal.views import index_view, pages_view

from django.urls import path, re_path

# app_name = 'internal'

urlpatterns = [
    # matches any html file
    re_path(r'^.*\.html', pages_view, name='pages'),
    path('', index_view, name='home'),
    path('login/', index_view, name='login'),
    path('register/', index_view, name='register'),
    path('logout/', index_view, name='logout')
]
