from django.urls import path
from . import views

app_name = 'loquendo'

urlpatterns = [
    path('', views.diversion, name='apppage'),
    path('<slug:slug>/', views.divertido, name='person'),
]