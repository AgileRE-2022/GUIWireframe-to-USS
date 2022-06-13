from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse
import uuid

from ..models import Context, Scenario, Wireframe
from ..functions.compdetector import *
from ..middleware import isGuest

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

    args['scenarios'] = Scenario.objects.filter(wireframe_id=id)
    return TemplateResponse(request, template, args)
