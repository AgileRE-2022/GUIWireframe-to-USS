from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse
import uuid

from .models import Context, Scenario, Wireframe
from .functions.compdetector import *

from .controllers.auth import *
from .controllers.wireframe import *
from .controllers.scenario import *


@csrf_protect
def context(request, id):
    args = {}
    template = 'project/context.html'
    return TemplateResponse(request, template, args)

def export(request, id):
    return HttpResponse('page export dengan id = ' + str(id))