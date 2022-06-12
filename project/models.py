from django.db import models


class Wireframe(models.Model):
    project_name = models.TextField(max_length=200)
    project_file = models.TextField(max_length=200)
    project_password = models.TextField()
    project_uid = models.CharField(max_length=200)
    project_us_purpose = models.CharField(max_length=200, null=True)
    project_us_user = models.CharField(max_length=200,  null=True)
    project_us_todo = models.CharField(max_length=200,  null=True)


class Scenario(models.Model):
    scenario_title = models.CharField(max_length=200)
    wireframe_id = models.CharField(max_length=200)


class Component(models.Model):
    type_component = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    wireframe_id = models.CharField(max_length=200)


class Context(models.Model):
    context_type = models.CharField(max_length=200)
    component_id = models.IntegerField(null=True)
    context_statement = models.CharField(max_length=200, null=True)
    scenario_id = models.IntegerField(null=True)
    context_template = models.CharField(max_length=200, null=True)

    def comp(self):
        return Component.objects.get(id=self.component_id)
