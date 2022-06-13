from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name="project_list"),
    path('create', views.create, name="project_create"),
    path('<int:id>/', include([
        path('', views.details, name="project_details"),
        path('download/', views.download, name="project_download"),
        path('rules/', include([
            path('add', views.rulesAdd, name="project_rules_add"),
            path('<int:rid>', views.rulesEdit, name="project_rules_edit"),
        ])),
        path('activity/', include([
            path('add', views.activityAdd, name="project_activiy_add"),
            path('<int:aid>', views.activityEdit, name="project_activiy_edit"),
        ])),
        path('context', views.context, name="project_context"),
        path('export', views.export, name="project_export"),
        path('delete/', include([
            path('rules/<del_id>', views.rulesDelete,
                 name="project_rules_delete"),
            path('event/<del_id>', views.activityDelete,
                 name="project_activity_delete"),
        ])),
        path('context/', include([
            path('given', views.ctxGiven, name="project_context_given"),
            path('when', views.ctxWhen, name="project_context_when"),
            path('then', views.ctxThen, name="project_context_then"),
            path('athen', views.ctxAThen, name="project_context_athen"),
        ])),
        path('scenario/', include([
            path('add', views.addScenario, name="project_scenario_add"),
        ])),
    ])),
    path('logout', views.logout, name="project_logout")
]
