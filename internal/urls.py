# from django.conf.urls import url
from internal.views import index_view, pages_view, login_view, register_user
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path

# app_name = 'internal'

urlpatterns = [
    # matches any html file
    re_path(r'^.*\.html', pages_view, name='pages'),
    path('', index_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', LogoutView.as_view(), name='logout')
]
