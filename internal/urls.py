from django.conf.urls import url
from internal.views import index_view

app_name = 'internal'

urlpatterns = [
    url(r'^$', index_view, name='index'),
]
