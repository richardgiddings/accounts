from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^transaction_screen/$', views.transaction_screen, name='transaction_screen'),
]