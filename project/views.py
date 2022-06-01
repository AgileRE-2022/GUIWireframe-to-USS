from pickletools import read_bytes1
from unicodedata import name
from django.http import HttpResponse
from django.template import loader
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse

from .models import Wireframe,Activity


def index(request):
    args = {}
    template = 'project/index.html'
    return TemplateResponse(request, template, args)


@csrf_protect
def create(request):
    if request.method == 'POST':
        # Validate Input Here
        if request.FILES['file']:
            file = request.FILES['file']
            print("nama file : " + file.name)
            # validator plant UML
            filename = file.name
            tipeFile = ["plantuml","PU","puml"]
            if filename.split('.')[-1] in tipeFile:
                print('is plant UML')
                arr = []
                for line in file:
                    arr.append(line.decode("utf-8")[0:-1])
                print(arr)
            else:
                print('is not plant UML')

        return redirect('project_list')
        # learn how to redirect with message
    else:
        template = loader.get_template('project/create.html')
        return render(request, "project/create.html")

# dapa
def details(request, id):
    # return HttpResponse('page details dengan id = '+ str(id))
    args = {}
    template = "project/details.html"
    args['id'] = id

    activity = Activity.objects.all()
    args['list_activites'] = activity
    return TemplateResponse(request, template, args)

# aril
@csrf_protect
def rulesAdd(request, id):
    args = {}
    if request.method == 'POST':
        rule = request.POST.get("rule")
        select = request.POST.get("select")
        if rule != "":
            print("nama rules adalah: " + rule)
        else:
            print("isilah dengan benar")
            # template = 'project/rules.html'
            # args['rules'] = ""
            # return TemplateResponse (request, template, args)
    
    template = 'project/rules.html'
    args['rules'] = ""
    return TemplateResponse (request, template, args)
    


def rulesEdit(request, id, rid):
    return HttpResponse('ini page rules edit dari id ='+str(id)+' dengan rules id = '+str(rid))

# rapid
@csrf_protect
def activityAdd(request,id):
    argActAdd= {}
    if request.method == 'POST':
        name = request.POST.get("Activity_name")
        component = request.POST.get("Component")
        if name is not None :
            # print("nama Activity "+ name +" dengan komponen yang di pilih : " + component)
            ac= Activity(wireframe_id=1, activity_name= name)
            if component is not "":
                ac.component_id = int(component)
            ac.save()
            return redirect('project_details',1)
        else:
            print("silahkan mengisi dengan benar")
        template = 'project/ActivityAdd.html'
        return TemplateResponse(request,template)
    else:
       template = 'project/ActivityAdd.html'
       return TemplateResponse(request,template)
    
    # return HttpResponse(template.render())
    # return HttpResponse('ini activity add dengan id = '+ str(id))

# @csrf_protect
def activityEdit(request, id, aid):
    act= Activity.objects.get(id=aid)
    if request.method == 'POST':
        act_name = request.POST.get("Activity_name")
        act_compo = request.POST.get("Component")
        act.activity_name= act_name
        if act_compo is not "" :
            act.component_id= act_compo
        else :
            act.component_id= None
        act.save()
        return redirect('project_details',1)
    # elif request.method == 'DELETE':
    #     print("delete berhasil")
    #     return redirect('project_details',1)

    argActEdit={}
    template = 'project/ActivityEdit.html'
    argActEdit['act'] = act
    # print(act.activity_name )
    return TemplateResponse(request,template,argActEdit)
    # return HttpResponse('ini page activity edit dari id ='+str(id)+' dengan activity id = '+str(aid))
def activityDelete(request,del_id):
    act_del= Activity.objects.get(id=del_id)
    act_del.delete()
    return redirect('project_details',1)
# ga dulu 
def context(request, id):
    args = {}
    template = 'project/context.html'
    return TemplateResponse(request, template, args)

def export(request, id):
    return HttpResponse('page export dengan id = '+ str(id))

