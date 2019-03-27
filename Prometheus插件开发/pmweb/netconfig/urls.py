from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'addconfig', views.addconfig, name='addconfig'),
    url(r'addNConfig', views.addconfigs, name='addconfigs'),
    url(r'getPConfig', views.getconfigs, name='getconfigs'),
]
