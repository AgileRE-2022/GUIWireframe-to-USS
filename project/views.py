from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse
import uuid

from .models import Wireframe, Rules, Activity
from .functions.compdetector import *


def index(request):
    args = {}
    template = 'project/index.html'
    args['projects'] = Wireframe.objects.all()
    return TemplateResponse(request, template, args)


@csrf_protect
def create(request):
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


def details(request, id):
    args = {}
    template = "project/details.html"
    args['id'] = id
    args['wireframe'] = Wireframe.objects.get(id=id)
    args['components'] = Component.objects.filter(wireframe_id=id)
    args['activities'] = Activity.objects.filter(wireframe_id=id)
    return TemplateResponse(request, template, args)


@csrf_protect
def rulesAdd(request, id):
    args = {}
    args['wireframe'] = Wireframe.objects.get(id=id)
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
    rules = Rules.objects.get(id=rid)
    args = {}
    args['wireframe'] = Wireframe.objects.get(id=id)
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


def rulesDelete(request, del_id):
    rules_del = Rules.objects.get(id=del_id)
    rules_del.delete()
    return redirect('project_details', 1)


@csrf_protect
def activityAdd(request, id):
    args = {}
    args['wireframe'] = Wireframe.objects.get(id=id)
    args['components'] = Component.objects.filter(wireframe_id=id)

    if request.method == 'POST':
        name = request.POST.get("Activity_name")
        component = request.POST.get("Component")
        if name is not None:
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
    args = {}
    args['wireframe'] = Wireframe.objects.get(id=id)
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


def activityDelete(request, del_id):
    act_del = Activity.objects.get(id=del_id)
    act_del.delete()
    return redirect('project_details', 1)


def context(request, id):
    args = {}
    template = 'project/context.html'
    return TemplateResponse(request, template, args)


def export(request, id):
    return HttpResponse('page export dengan id = ' + str(id))
