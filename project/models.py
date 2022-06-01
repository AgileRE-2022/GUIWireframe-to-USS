from django.db import models

# Create your models here.
class Wireframe(models.Model):
    project_name = models.TextField(max_length=200)
    project_file = models.TextField(max_length=200)
    project_password = models.TextField()
    project_uid = models.CharField(max_length=200)

class Component(models.Model):
    type_component = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    wireframe_id = models.CharField(max_length=200)
    def rules(self):
        return Rules.objects.filter(component_id=self.id)
    
class Rules(models.Model):
    component_id = models.IntegerField()
    rules_desc = models.CharField(max_length=200)

class Activity(models.Model):
    wireframe_id  = models.IntegerField()
    activity_name = models.CharField(max_length=200)
    component_id  = models.IntegerField(null=True)
    def comp(self):
        return Component.objects.get(id=self.component_id)
