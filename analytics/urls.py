from django.conf.urls import url
from . import views

urlpatterns = [
				url(r'^goods/$', views.goods, name='goods'),
                url(r'^cash/$', views.cash, name='cash'),
                url(r'^demographic/$', views.demographic, name='demographic')

]