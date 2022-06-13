from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect

from ..models import Context, Scenario
from ..functions.compdetector import *

@csrf_protect
def addScenario(request, id):
    if request.method == "POST":
        scenario = request.POST.get("scenario")
        given_template = request.POST.get("given-template")
        given_statement = request.POST.get("given-statement")
        when_template = request.POST.get("when-template")
        when_statement = request.POST.get("when-statement")
        when_component = request.POST.get("when-component")
        then_template = request.POST.get("then-template")
        then_statement = request.POST.get("then-statement")
        then_component = request.POST.get("then-component")

        s = Scenario(
            wireframe_id=request.session["project"],
            scenario_title=scenario
        )
        s.save()

        g = Context(
            context_type="given",
            component_id=None,
            context_statement=given_statement,
            scenario_id=s.id,
            context_template=given_template,
        )
        g.save()

        if when_statement == "":
            when_statement = None
        if when_component == "":
            when_component = None
        w = Context(
            context_type="when",
            component_id=when_component,
            context_statement=when_statement,
            scenario_id=s.id,
            context_template=when_template,
        )
        w.save()

        if then_statement == "":
            then_statement = None
        if then_component == "":
            then_component = None
        t = Context(
            context_type="then",
            component_id=then_component,
            context_statement=then_statement,
            scenario_id=s.id,
            context_template=then_template,
        )
        t.save()

    return redirect('project_details', request.session["project"])


@csrf_protect
def editScenario(request, id):
    if request.method == "POST":
        edit_type = request.POST.get("edit_type")
        if edit_type == "scenario":
            s = Scenario.objects.get(id=request.POST.get("s_id"))
            s.scenario_title = request.POST.get("scenario")
            s.save()
        elif edit_type == "scenario-delete":
            s = Scenario.objects.get(id=request.POST.get("s_id"))
            s.delete()
        elif edit_type == "add-given":
            c = Context(
                context_type="given",
                component_id=None,
                context_statement=request.POST.get("given-statement"),
                scenario_id=request.POST.get("s_id"),
                context_template=request.POST.get("given-template"),
            )
            c.save()
        elif edit_type == "edit-given":
            c = Context.objects.get(id=request.POST.get("s_id"))
            c.context_statement = request.POST.get("given-statement")
            c.context_template = request.POST.get("given-template")
            c.save()
        elif edit_type == "delete-given":
            c = Context.objects.get(id=request.POST.get("s_id"))
            c.delete()
        elif edit_type == "add-when":
            c = Context(
                context_type="when",
                component_id=request.POST.get('when-component'),
                context_statement=request.POST.get("when-statement"),
                scenario_id=request.POST.get("s_id"),
                context_template=request.POST.get("when-template"),
            )
            c.save()
        elif edit_type == "edit-when":
            when_component = request.POST.get("when-component")
            when_statement = request.POST.get("when-statement")
            if when_statement == "":
                when_statement = None
            if when_component == "":
                when_component = None
            c = Context.objects.get(id=request.POST.get("s_id"))
            c.component_id = when_component
            c.context_statement = when_statement
            c.context_template = request.POST.get("when-template")
            c.save()
        elif edit_type == "delete-when":
            c = Context.objects.get(id=request.POST.get("s_id"))
            c.delete()
        elif edit_type == "add-then":
            c = Context(
                context_type="then",
                component_id=None,
                context_statement=request.POST.get("then-statement"),
                scenario_id=request.POST.get("s_id"),
                context_template=request.POST.get("then-template"),
            )
            c.save()
        elif edit_type == "edit-then":
            then_component = request.POST.get("then-component")
            then_statement = request.POST.get("then-statement")
            if then_statement == "":
                then_statement = None
            if then_component == "":
                then_component = None
            c = Context.objects.get(id=request.POST.get("s_id"))
            c.component_id = then_component
            c.context_statement = then_statement
            c.context_template = request.POST.get("then-template")
            c.save()
        elif edit_type == "delete-then":
            c = Context.objects.get(id=request.POST.get("s_id"))
            c.delete()

    return redirect('project_details', request.session["project"])
