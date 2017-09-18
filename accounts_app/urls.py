from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^transaction_screen/$', views.transaction_screen, name='transaction_screen'),
    url(r'^view_account/(?P<account_number>\d+)$', views.view_account, name='view_account'),
    url(r'^payment/$', views.payment, name='payment'),
]