from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="project_list"),
    path('create', views.create, name="project_create"),
    path('test', views.index, name="testView"),
]
