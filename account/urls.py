from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^create-user/$', views.create_user, name='create_user'),
    url(r'^add-users$', views.add_users, name='add_users'),
    url(r'^add-refugee$', views.add_refugee, name='add_refugee'),
    url(r'^add-merchant$', views.add_merchant, name='add_merchant'),
    url(r'^add-partner-user$', views.add_partner_user, name='add_partner_user'),
    url(r'^activate-account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
    views.activate_account, name='activate_account'),
    url(r'^add-trucker', views.add_trucker, name='add_trucker'),
    url(r'^kodhi-login/', views.kodhi_login, name='kodhi_login'),
    url(r'^enter-token/$', views.enter_token, name='enter_token'),
    url('^', include('django.contrib.auth.urls')),
]