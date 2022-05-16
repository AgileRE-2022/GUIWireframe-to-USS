from django.http import HttpResponse
from django.template import loader

from .models import Wireframe


def index(request):
    template = loader.get_template('project/index.html')
    return HttpResponse(template.render())


def create(request):
    if request.method == 'POST':
        # uji disini
        return HttpResponse("TEST")
    else:
        template = loader.get_template('project/create.html')
        return HttpResponse(template.render())
