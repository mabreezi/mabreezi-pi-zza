from django.conf.urls import url
from . import views

urlpatterns = [
                url(r'^send-location/(?P<shipment_number>[0-9]+)/$', views.send_location, name='send_location')

]