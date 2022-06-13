from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse
import uuid

from .models import Context, Scenario, Wireframe
from .functions.compdetector import *
from .middleware import isGuest


@csrf_protect
def index(request):
    args = {}

    if not isGuest(request):
        return redirect('project_details', request.session["project"])

    if request.method == "POST":
        w = Wireframe.objects.get(id=request.POST.get("id"))
        if w.project_password == request.POST.get("password"):
            request.session["project"] = w.id
            request.session["project_name"] = w.project_name
            return redirect('project_details', w.id)

    template = 'project/index.html'
    args['projects'] = Wireframe.objects.all()
    return TemplateResponse(request, template, args)


def logout(request):
    try:
        del request.session["project"]
        del request.session["project_name"]
    except KeyError:
        pass
    return redirect('project_list')


@csrf_protect
def create(request):
    if not isGuest(request):
        return redirect('project_details', request.session["project"])

    if request.method == 'POST':
        # Validate Input Here
        name = request.POST.get('project_name')
        password = request.POST.get('project_password')
        purpose = request.POST.get('project_purpose')
        user = request.POST.get('project_user')
        todo = request.POST.get('project_todo')
        filecontent = request.POST.get('saltScript')

        w = Wireframe(
            project_name=name,
            project_password=password,
            project_file=filecontent,
            project_uid=str(uuid.uuid4()),
            project_us_purpose=purpose,
            project_us_user=user,
            project_us_todo=todo)
        w.save()

        arr = str(filecontent).splitlines()
        arrbersih = bersih(arr)
        print(arrbersih)
        inspectcomp(arrbersih, w.id)
        return redirect('project_list')

    else:
        args = {}
        template = 'project/create.html'
        return TemplateResponse(request, template, args)


@csrf_protect
def details(request, id):
    if isGuest(request):
        return redirect('project_list')
    elif request.session["project"] != id:
        return redirect('project_list')

    args = {}
    template = "project/details.html"
    args['wireframe'] = Wireframe.objects.get(id=id)
    args['components'] = Component.objects.filter(wireframe_id=id)

    # ctx = {}
    # ctx["given"] = Context.objects.filter(context_type="given")
    # ctx["athen"] = Context.objects.filter(context_type="alt-then")
    # ctx["when"] = Context.objects.filter(context_type="when")
    # ctx["then"] = Context.objects.filter(context_type="then")

    # args["context"] = ctx

    args['scenarios'] = Scenario.objects.filter(wireframe_id=id)
    return TemplateResponse(request, template, args)


@csrf_protect
def rulesAdd(request, id):
    if isGuest(request):
        return redirect('project_list')
    elif request.session["project"] != id:
        return redirect('project_list')

    args = {}
    args['components'] = Component.objects.filter(wireframe_id=id)

    if request.method == 'POST':
        rule = request.POST.get("rule")
        select = request.POST.get("select")
        if rule != "":
            print("nama rules adalah: " + rule)
            r = Rules(rules_desc=rule, component_id=int(select))
            r.save()
            return redirect('project_details', id)
        else:
            print("isilah dengan benar")

    template = 'project/rules.html'
    return TemplateResponse(request, template, args)


@csrf_protect
def rulesEdit(request, id, rid):
    if isGuest(request):
        return redirect('project_list')
    elif request.session["project"] != id:
        return redirect('project_list')

    rules = Rules.objects.get(id=rid)
    args = {}
    args['components'] = Component.objects.filter(wireframe_id=id)

    if request.method == 'POST':
        rules.rules_desc = request.POST.get("rule")
        rules.component_id = request.POST.get("select")
        rules.save()
        return redirect('project_details', id)

    elif request.method == 'DELETE':
        print('Delete dijalankan')
        rules.delete()
        return redirect('project_details', id)

    template = 'project/rulesEdit.html'
    args['rule'] = rules

    return TemplateResponse(request, template, args)


def rulesDelete(request, id, del_id):
    if isGuest(request):
        return redirect('project_list')
    elif request.session["project"] != id:
        return redirect('project_list')

    rules_del = Rules.objects.get(id=del_id)
    rules_del.delete()
    return redirect('project_details', 1)


@csrf_protect
def activityAdd(request, id):
    if isGuest(request):
        return redirect('project_list')
    elif request.session["project"] != id:
        return redirect('project_list')

    args = {}
    args['components'] = Component.objects.filter(wireframe_id=id)

    if request.method == 'POST':
        name = request.POST.get("Activity_name")
        component = request.POST.get("Component")
        if name != None and component != None:
            # print("nama Activity "+ name +" dengan komponen yang di pilih : " + component)
            ac = Activity(wireframe_id=id, activity_name=name)
            if component != "":
                ac.component_id = int(component)
            ac.save()
            return redirect('project_details', id)
        else:
            print("silahkan mengisi dengan benar")

    template = 'project/ActivityAdd.html'
    return TemplateResponse(request, template, args)


@csrf_protect
def activityEdit(request, id, aid):
    if isGuest(request):
        return redirect('project_list')
    elif request.session["project"] != id:
        return redirect('project_list')

    args = {}
    args['components'] = Component.objects.filter(wireframe_id=id)
    act = Activity.objects.get(id=aid)

    if request.method == 'POST':
        act_name = request.POST.get("Activity_name")
        act_compo = request.POST.get("Component")
        act.activity_name = act_name

        if act_compo != "":
            act.component_id = act_compo
        else:
            act.component_id = None

        act.save()
        return redirect('project_details', id)

    template = 'project/ActivityEdit.html'
    args['act'] = act
    return TemplateResponse(request, template, args)


def activityDelete(request, id, del_id):
    if isGuest(request):
        return redirect('project_list')
    elif request.session["project"] != id:
        return redirect('project_list')

    act_del = Activity.objects.get(id=del_id)
    act_del.delete()
    return redirect('project_details', 1)


@csrf_protect
def context(request, id):
    args = {}
    template = 'project/context.html'
    return TemplateResponse(request, template, args)


def export(request, id):
    return HttpResponse('page export dengan id = ' + str(id))


@csrf_protect
def ctxGiven(request, id):
    statement = request.POST.get("statement")
    component = request.POST.get("component")
    delete = request.POST.get("delete")
    c_id = request.POST.get("c_id")

    if c_id != None and c_id != "" and delete != None and delete == "true":
        c = Context.objects.get(id=c_id)
        print("Delete")
        c.delete()
        return redirect('project_details', request.session["project"])

    if statement != None and component != None:
        if c_id != None and c_id != "":
            c = Context.objects.get(id=c_id)
            if component is "":
                c.component_id = None
            else:
                c.component_id = component
            c.context_statement = statement
            c.save()
        else:
            if component == "":
                component = None
            c = Context(
                wireframe_id=request.session["project"],
                context_type="given",
                component_id=component,
                activity_id=None,
                context_conjunction="for",
                context_statement=statement
            )
            c.save()
    return redirect('project_details', request.session["project"])


@csrf_protect
def ctxWhen(request, id):
    statement = request.POST.get("statement")
    rule = request.POST.get("rule")
    conjunction = request.POST.get("conjunction")
    c_id = request.POST.get("c_id")
    delete = request.POST.get("delete")

    if c_id != None and c_id != "" and delete != None and delete == "true":
        c = Context.objects.get(id=c_id)
        c.delete()
        return redirect('project_details', request.session["project"])

    if statement != None and rule != None and conjunction != None:
        if c_id != None and c_id != "":
            c = Context.objects.get(id=c_id)
            c.rule_id = rule
            c.context_conjunction = conjunction
            c.context_statement = statement
            c.save()
        else:
            c = Context(
                wireframe_id=request.session["project"],
                context_type="when",
                component_id=None,
                rule_id=rule,
                activity_id=None,
                context_conjunction=conjunction,
                context_statement=statement
            )
        c.save()
    return redirect('project_details', request.session["project"])


@csrf_protect
def ctxThen(request, id):
    activity = request.POST.get("activity")
    tipe = request.POST.get("type")
    delete = request.POST.get("delete")
    c_id = request.POST.get("c_id")

    if c_id != None and c_id != "" and delete != None and delete == "true":
        c = Context.objects.get(id=c_id)
        print("Delete")
        c.delete()
        return redirect('project_details', request.session["project"])

    if activity is not None and tipe is not None:
        if c_id is not None and c_id is not "":
            c = Context.objects.get(id=c_id)
            c.activity_id = activity
            c.save()
        else:
            c = Context(
                wireframe_id=request.session["project"],
                context_type=tipe,
                component_id=None,
                activity_id=activity,
                context_conjunction=None,
                context_statement=None
            )
            c.save()
    return redirect('project_details', request.session["project"])


@csrf_protect
def ctxAThen(request, id):
    activity = request.POST.get("activity")
    type = request.POST.get("type")
    c_id = request.POST.get("c_id")
    delete = request.POST.get("delete")

    if c_id != None and delete != None and delete == "true":
        c = Context.objects.get(id=c_id)
        c.delete()
        return redirect('project_details', request.session["project"])

    if activity != None and type != None:
        if c_id != None and c_id != "":
            c = Context.objects.get(id=c_id)
            c.activity_id = activity
            c.save()
        else:
            c = Context(
                wireframe_id=request.session["project"],
                context_type=type,
                activity_id=activity,
            )
            c.save()
    return redirect('project_details', request.session["project"])


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
            print(c)
            print(request.POST.get("given-statement"))
            print(request.POST.get("given-template"))
            c.context_statement = request.POST.get("given-statement")
            c.context_template = request.POST.get("given-template")
            c.save()
        elif edit_type == "delete-given":
            c = Context.objects.get(id=request.POST.get("s_id"))
            c.delete()

    return redirect('project_details', request.session["project"])
