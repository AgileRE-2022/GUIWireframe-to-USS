from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse
import uuid

from .models import Context, Wireframe, Rules, Activity
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
        filecontent = ""
        if request.FILES['file']:
            file = request.FILES['file']
            print("nama file : " + file.name)
            # validator plant UML
            filename = file.name
            tipeFile = ["plantuml", "PU", "puml"]
            if filename.split('.')[-1] in tipeFile:
                print('is plant UML')
                arr = []
                for line in file:
                    filecontent += line.decode("utf-8")
                    arr.append(line.decode("utf-8"))
                print(arr)

                w = Wireframe(
                    project_name=name,
                    project_password=password,
                    project_file=filecontent,
                    project_uid=str(uuid.uuid4()))
                w.save()

                arrbersih = bersih(arr)
                print(arrbersih)
                inspectcomp(arrbersih, w.id)
            else:
                print('is not plant UML')

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
    args['activities'] = Activity.objects.filter(wireframe_id=id)

    ctx = {}
    ctx["given"] = Context.objects.filter(context_type="given")
    ctx["then"] = Context.objects.filter(context_type="then")

    args["context"] = ctx
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
        if name is not None and component is not None:
            # print("nama Activity "+ name +" dengan komponen yang di pilih : " + component)
            ac = Activity(wireframe_id=id, activity_name=name)
            if component is not "":
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

        if act_compo is not "":
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
    c_id = request.POST.get("c_id")
    if statement is not None and component is not None:
        if c_id is not None and c_id is not "":
            c = Context.objects.get(id=c_id)
            if component is "":
                c.component_id = None
            else:
                c.component_id = component
            c.context_statement = statement
            c.save()
        else:
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
    component = request.POST.get("component")
    conjunction = request.POST.get("conjunction")
    c_id = request.POST.get("c_id")
    if statement is not None and component is not None and conjunction is not None:
        if c_id is not None and c_id is not "":
            c = Context.objects.get(id=c_id)
            c.component_id = component
            c.context_conjunction = conjunction,
            c.context_statement = statement
            c.save()
        else:
            c = Context(
                wireframe_id=request.session["project"],
                context_type="when",
                component_id=component,
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
    c_id = request.POST.get("c_id")
    if activity is not None and tipe is not None:
        if c_id is not None and c_id is not "":
            c = Context.objects.get(id=c_id)
            c.activity_id = activity,
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
