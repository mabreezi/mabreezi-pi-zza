from django.conf.urls import url
from . import views

urlpatterns = [
				url(r'^add-person/$', views.add_person, name='add_person'),
				url(r'^add-item/$', views.add_item, name='add_item'),
				url(r'^submit-transaction/$', views.submit_transaction, name='submit_transaction'),
				url(r'^make-trade/$', views.make_trade, name='make_trade'),
				url(r'^participants/$', views.participants, name='participants'),
				]