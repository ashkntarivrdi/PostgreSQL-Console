from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_app, name='signup'),
    path('login/', views.login_app, name='login'),
]