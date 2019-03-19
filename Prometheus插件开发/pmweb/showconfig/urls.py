from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'showGroup$', views.showGroup, name='showGroup'),
    url(r'showGroupInfo$', views.showGroupInfo, name='showGroupInfo'),
    url(r'updateGroupInfo$', views.updateGroupInfo, name='updateGroupInfo'),
    url(r'delGroupInfo$', views.delGroupInfo, name='updateGroupInfo'),
    url(r'showHost$', views.showHost, name='showHost'),
    url(r'showHostInfo$', views.showHostInfo, name='showHostInfo'),
]
