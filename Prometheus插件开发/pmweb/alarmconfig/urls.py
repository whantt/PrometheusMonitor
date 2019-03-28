from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'toAlarm', views.toAlarm, name='toAlarm'),
    url(r'getAlarm', views.getAlarm, name='getAlarm'),
    url(r'submitAlarm', views.submitAlarm, name='submitAlarm'),
    url(r'delAlarm', views.delAlarm, name='delAlarm')
]
