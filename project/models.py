from msilib.schema import Component
from pyexpat import model
from statistics import mode
from django.db import models

# Create your models here.
class Wireframe(models.Model):
    project_name = models.TextField(max_length=200)
    project_file = models.TextField(max_length=200)
    project_password = models.TextField()
    project_uid = models.CharField(max_length=200)

class Activity(models.Model):
    wireframe_id  = models.IntegerField()
    activity_name = models.CharField(max_length=200)
    #insull
    component_id  = models.IntegerField(null=True)