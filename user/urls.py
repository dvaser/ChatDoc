from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.signin, name='login'),
    path('register/', views.signup, name='register'),
    path('register/verify/', views.verifyCode, name='verify'),
    path('logout/', views.signout, name='logout'),
    path('password/forget/', views.pswForget, name='pswForget'),
    path('delete-account/', views.delete_account, name='delete-account'),
]
