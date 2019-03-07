from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$', views.loginUser, name='loginUser'),
    url(r'show$', views.show, name='show'),
    url(r'showGroup$', views.showGroup, name='showGroup'),
    url(r'showHost$', views.showHost, name='showHost'),
    url(r'showPConfig', views.showPConfig, name='showPConfig'),
    url(r'showK$', views.showK, name='showK'),
    url(r'getPConfig', views.getPConfig, name='getPConfig'),
    url(r'addPConfig', views.addPConfig, name='addPConfig'),
    url(r'addGConfig', views.addGConfig, name='addGConfig'),
    url(r'addHConfig', views.addHConfig, name='addHConfig'),
    url(r'updatePConfig', views.updatePConfig, name='updatePConfig'),
    # url(r'addGroup', views.addGroup, name='addGroup'),
    # url(r'addHost', views.addHost, name='addHost'),
]
