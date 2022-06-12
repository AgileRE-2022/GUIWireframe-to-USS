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

    def given(self):
        return Context.objects.filter(scenario_id=self.id, context_type="given")

    def when(self):
        return Context.objects.filter(scenario_id=self.id, context_type="when")

    def then(self):
        return Context.objects.filter(scenario_id=self.id, context_type="then")


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

    def text(self):
        fcomp = self.context_template
        if self.context_statement != None and fcomp.find("<statement>") >= 0:
            s = self.context_statement
            fcomp = fcomp.replace("<statement>", self.context_statement)
        if self.component_id != None and fcomp.find("<component>") >= 0:
            c = self.comp()
            fcomp = fcomp.replace("<component>", c.type_component + " " + c.value)
        return fcomp
