"""pmweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from pmweb import settings
from . import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'toMain/', views.toMain, name='toMain'),
    url(r'first/', views.firstPage, name='firstPage'),
    url(r'refresh/', views.refresh, name='refresh'),
    url(r'^prometheusconfig/', include('addconfig.urls')),
    url(r'^prometheusinfo/', include('showconfig.urls')),
    url(r'^addrule/', include('addrules.urls')),
    url(r'^showrule/', include('showrules.urls')),
    url(r'^netconfig/', include('netconfig.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT,
        }),
]
