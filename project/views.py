
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
