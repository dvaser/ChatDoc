from django.urls import path
from . import views
from .views import custom_404

urlpatterns = [
    path('', views.chat, name='chat'),
]

handler404 = custom_404