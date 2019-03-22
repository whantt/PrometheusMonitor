from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'createRules', views.createRules, name='createRules'),
    url(r'dealRules', views.dealRules, name='dealRules'),
    url(r'cloneRules', views.cloneRules, name='cloneRules'),
    url(r'getRulesModel', views.getRulesModel, name='getRulesModel'),
    url(r'addApplication', views.addApplication, name='addApplication'),
    url(r'getApplication', views.getApplication, name='getApplication'),
    url(r'addRules', views.addRules, name='addRules'),
    url(r'getAllGroups', views.getAllGroups, name='getAllGroups'),
    url(r'getAllHosts', views.getAllHosts, name='getAllHosts'),
    url(r'addAllRules', views.addAllRules, name='addAllRules'),
    url(r'getRuleModel', views.getRuleModel, name='getRuleModel'),
    url(r'updateRuleModel', views.updateRuleModel, name='updateRuleModel'),
    url(r'submitClone', views.submitClone, name='submitClone'),
]
