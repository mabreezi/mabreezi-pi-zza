from django.conf.urls import url
from . import views

urlpatterns = [
				# url(r'^add-person/$', views.add_person, name='add_person'),
				url(r'^add-item/$', views.add_item, name='add_item'),
				url(r'^submit-transaction/$', views.submit_transaction, name='submit_transaction'),
				url(r'^make-trade/$', views.make_trade, name='make_trade'),
				# url(r'^participants/$', views.participants, name='participants'),
				url(r'^dashboard/$', views.dashboard, name='dashboard'),
				url(r'^$', views.login_page, name='login_page'),
				url(r'^item-detail/(?P<item_id>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})/$', 
				views.get_item_detail, name = 'item_detail'),
				url(r'^add-shipment', views.add_shipment, name='add_shipment'),
				url(r'^shipment-detail/(?P<shipment_number>[0-9]+)/$', views.get_shipment_detail, name='shipment_detail')
				]