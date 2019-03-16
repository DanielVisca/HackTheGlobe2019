from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('sms_response/', views.sms_response, name='sms_response'),
	#url(r'^$', views.sms_response, name='sms_response'),
]