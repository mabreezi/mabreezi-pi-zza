from django.conf.urls import url
from . import views

urlpatterns = [
                url(r'^send-location/$', views.send_location, name='send_location')

]