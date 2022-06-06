from django.db import models


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
    def comp(self):
        return Component.objects.get(id=self.component_id)

class Activity(models.Model):
    wireframe_id = models.IntegerField()
    activity_name = models.CharField(max_length=200)
    component_id = models.IntegerField(null=True)

    def comp(self):
        return Component.objects.get(id=self.component_id)


class Context(models.Model):
    wireframe_id = models.IntegerField()
    context_type = models.CharField(max_length=200)
    component_id = models.IntegerField(null=True)
    rule_id = models.IntegerField(null=True)
    activity_id = models.IntegerField(null=True)
    context_conjunction = models.CharField(max_length=20, null=True)
    context_statement = models.CharField(max_length=200, null=True)

    def comp(self):
        return Component.objects.get(id=self.component_id)

    def activity(self):
        return Activity.objects.get(id=self.activity_id)
        
    def rule(self):
        return Rules.objects.get(id=self.rule_id)
