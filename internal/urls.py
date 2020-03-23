from django.conf.urls import url
from internal.views import index_view, pages_view

from django.urls import path, re_path

app_name = 'internal'

urlpatterns = [
    # matches any html file
    re_path(r'^.*\.html', pages_view, name='page'),
    url(r'^$', index_view, name='index'),
]
