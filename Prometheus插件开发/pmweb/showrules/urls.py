from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'showModelRule$', views.showModelRule, name='showModelRule'),
    url(r'showRule$', views.showRule, name='showRule'),
    url(r'getAllRules$', views.getAllRules, name='getAllRules'),
    url(r'getRuleInfo', views.getRuleInfo, name='getRuleInfo'),
    url(r'updateRuleInfo', views.updateRuleInfo, name='updateRuleInfo'),
]
