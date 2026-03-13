from django.urls import path
from django.shortcuts import redirect

urlpatterns = [
    # Временно перенаправляем все на каталог
    path('', lambda request: redirect('catalog'), name='home'),
    path('contacts/', lambda request: redirect('catalog'), name='contacts'),
]