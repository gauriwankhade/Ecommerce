
from django.urls import path
from .views import registerView,loginView,signoutView,profileView,accountView,orderHistoryView


urlpatterns = [
	path('',profileView,name='profile_url'),
	path('register',registerView,name='register_url'),
	path('login',loginView,name='login_url'),
	path('logout',signoutView,name='logout_url'),
	path('account',accountView,name='account_url'),
	path('account/history',orderHistoryView,name='orderhistory'),

    
]
