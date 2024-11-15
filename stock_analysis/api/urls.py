from django.urls import path
from . import views

urlpatterns = [
    path('create-superuser-and-load-fixtures/', views.create_superuser_and_load_fixtures, name='create_superuser_and_load_fixtures'),
]