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

    if request.method == "POST":
        if request.POST.get('mode') == 'delete':
            w = Wireframe.objects.get(id=id)
            w.delete()
            return redirect('project_logout')
        elif request.POST.get('mode') == 'edit':
            name = request.POST.get('project_name')
            purpose = request.POST.get('project_purpose')
            user = request.POST.get('project_user')
            todo = request.POST.get('project_todo')
            filecontent = request.POST.get('saltScript')

            wireframe = Wireframe.objects.get(id=id)
            wireframe.project_name = name

            if wireframe.project_file != filecontent :
                wireframe.project_file = filecontent

                c = Component.objects.filter(wireframe_id=id)
                for component in c:
                    component.delete()

                scenes = Scenario.objects.filter(wireframe_id=id)
                for scene in scenes:
                    ctx = Context.objects.filter(scenario_id=scene.id)
                    for context in ctx:
                        context.delete()
                    scene.delete()

                arr = str(filecontent).splitlines()
                arrbersih = bersih(arr)
                inspectcomp(arrbersih, wireframe.id)
                print("component change")



            wireframe.project_us_purpose = purpose
            wireframe.project_us_user = user
            wireframe.project_us_todo = todo
            wireframe.save()
            print("FINISH")
            request.session["project_name"] = name
            return redirect('project_details', id)

    args = {}
    template = "project/details.html"
    args['wireframe'] = Wireframe.objects.get(id=id)
    args['components'] = Component.objects.filter(wireframe_id=id)

    args['scenarios'] = Scenario.objects.filter(wireframe_id=id)

    return TemplateResponse(request, template, args)
