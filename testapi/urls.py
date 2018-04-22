"""testapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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

urlpatterns = [
    url(r'app/^admin/', admin.site.urls),
    url(r'^app/', include('hyper.urls', namespace='hyper')),
    url(r'^app/account/', include('account.urls', namespace='account')),
    url(r'^app/location/', include('location.urls', namespace='location')),
    url(r'^app/analytics/', include('analytics.urls', namespace='analytics'))
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
