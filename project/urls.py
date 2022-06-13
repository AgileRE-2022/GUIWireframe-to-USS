from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name="project_list"),
    path('create', views.create, name="project_create"),
    path('<int:id>/', include([
        path('', views.details, name="project_details"),
        path('context', views.context, name="project_context"),
        path('export', views.export, name="project_export"),
        path('scenario/', include([
            path('add', views.addScenario, name="project_scenario_add"),
            path('edit', views.editScenario, name="project_scenario_edit"),
        ])),
    ])),
    path('logout', views.logout, name="project_logout")
]
