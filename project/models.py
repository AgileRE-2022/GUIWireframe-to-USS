from pyexpat import model
from statistics import mode
from django.db import models

# Create your models here.
class Wireframe(models.Model):
    project_name = models.TextField(max_length=200)
    project_file = models.TextField(max_length=200)
    project_password = models.TextField()
    project_uid = models.CharField(max_length=200)

class Rules(models.Model):
    component_id = models.IntegerField()
    rules_desc = models.CharField(max_length=200)
