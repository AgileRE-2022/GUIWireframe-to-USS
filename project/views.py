
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from .models import Wireframe


def index(request):
    template = loader.get_template('project/index.html')
    return HttpResponse(template.render())


@csrf_protect
def create(request):
    if request.method == 'POST':
        template = loader.get_template('project/post.html')
        # Validate Input Here
        if request.FILES['file']:
            file1 = request.FILES['file'].read()
            print(file1)
            # Validate File can start here

        return redirect('project_list')
        # learn how to redirect with message
    else:
        template = loader.get_template('project/create.html')
        return render(request, "project/create.html")
