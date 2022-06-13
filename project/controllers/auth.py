from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse

from ..models import Wireframe
from ..functions.compdetector import *
from ..middleware import isGuest


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