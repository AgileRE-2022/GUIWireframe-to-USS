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

class Activty(models.Model):
    wireframe_id  = models.IntegerField(max_length=200)
    Activity_name = models.CharField(max_length=200)
    #insull
    Component_id  = models.IntegerField(null=True,max_length=200)