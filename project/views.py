from django.http import HttpResponse
from django.template import loader
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse
import uuid

from .models import Wireframe


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
            tipeFile = ["plantuml","PU","puml"]
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
def activityAdd(request,id):
    argActAdd= {}
    template = 'project/ActivityAdd.html'
    return TemplateResponse(request,template)
    # return HttpResponse(template.render())
    # return HttpResponse('ini activity add dengan id = '+ str(id))

def activityEdit(request, id, aid):
    argActEdit={}
    template = 'project/ActivityEdit.html'
    return TemplateResponse(request,template)
    # return HttpResponse('ini page activity edit dari id ='+str(id)+' dengan activity id = '+str(aid))

# ga dulu 
def context(request, id):
    args = {}
    template = 'project/context.html'
    return TemplateResponse(request, template, args)

def export(request, id):
    return HttpResponse('page export dengan id = '+ str(id))

