from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'tofederal', views.tofederal, name='tofederal'),
    url(r'addfederal', views.addfederal, name='addfederal'),
    url(r'delFederal', views.delFederal, name='delFederal'),
    url(r'updateFederal', views.updateFederal, name='updateFederal'),
]
