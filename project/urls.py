from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="project_list"),
    path('create', views.create, name="project_create"),
    path('<int:id>/', views.details, name="project_details"),
    path('<int:id>/rules/add', views.rulesAdd, name="project_rules_add"),
    path('<int:id>/rules/<int:rid>/', views.rulesEdit, name="project_rules_edit"),
    path('<int:id>/activity/add', views.activityAdd, name="project_activiy_add"),
    path('<int:id>/activity/<int:aid>/', views.activityEdit, name="project_activiy_edit"),
    path('<int:id>/context', views.context, name="project_context"),
    path('<int:id>/export', views.export, name="project_export"),
    path('<int:id>/delete_rules/<del_id>', views.rulesDelete, name="project_rules_delete"),
    path('<int:id>/delete_event/<del_id>',views.activityDelete,name="project_activity_delete"),
    path('logout', views.logout, name="project_logout")
]
