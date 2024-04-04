from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.index, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    
]