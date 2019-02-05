from sobstvennik import settings
from django.conf.urls.static import  static
"""sobstvennik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    #url(r'^objects/$', views.objects),
    url(r'^about/$', views.about),
    url(r'^objects/$', views.AllObjects.as_view()),
    #url(r'^objects/(?P<pk>\d+)/$', views.Robject.as_view()),
    url(r'^objects/(?P<pk>\d+)/$', views.Robject.as_view()),
    url(r'^news/(?P<pk>\d+)/$', views.Nobject.as_view()),

    #url(r'^objects/(?P<page>\d+)/$', views.All_Objects.as_view()),



]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
