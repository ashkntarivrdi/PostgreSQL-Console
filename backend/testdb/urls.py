from django.urls import path
from . import views
from testdb import metrics  

urlpatterns = [
    path('app/', views.create_app, name='create_app'),
    path('app/<int:app_id>/', views.separator, name='separator'),
    path('apps/', views.list_apps, name='list_apps'),
    path('metrics/', metrics.metrics_view, name='metrics'),
]