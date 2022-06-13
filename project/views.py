from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_protect

import mimetypes
import os

from .models import Scenario, Wireframe
from .functions.compdetector import *

from .controllers.auth import *
from .controllers.wireframe import *
from .controllers.scenario import *


def download(request, id):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filenametemp = 'usstemp.txt'
    filename = 'uss.feature'
    # Define the full file path
    filepathtemp = BASE_DIR + '/project/functions/' + filenametemp  # template
    filepath = BASE_DIR + '/project/functions/' + filename  # ini yang di download

    # disini ambil variabel, trs write file
    wireframe = Wireframe.objects.get(id=id)
    scenario = Scenario.objects.filter(wireframe_id=id)

    file1 = open(filepathtemp, "r")
    text = file1.read()
    a = "\tIn order to " + wireframe.project_us_purpose
    b = "\tAs a " + wireframe.project_us_user
    c = "\tI want to " + wireframe.project_us_todo

    text = text.replace('<a>', a)
    text = text.replace('<b>', b)
    text = text.replace('<c>', c)
    p = ""
    for scene in scenario:
        s = "\tScenario: " + scene.scenario_title + "\n"
        p += s
        c = 1
        for given in scene.given():
            if c == 1:
                g = "Given "
            else:
                g = "And "
            isi = given.uss()
            p += "\t\t" + g + isi + "\n"
            c += 1
        c = 1
        for when in scene.when():
            if c == 1:
                w = "When "
            else:
                w = "And "
            isi = when.uss()
            p += "\t\t" + w + isi + "\n"
            c += 1
        c = 1
        for then in scene.then():
            if c == 1:
                t = "Then "
            else:
                t = "And "
            isi = then.uss()
            p += "\t\t" + t + isi + "\n"
            c += 1
        p += "\n"
    text = text.replace('<s>', p)

    # write file dari data diatas
    file = open(filepath, 'w')
    file.write(text)
    file.close()

    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % request.session["project_name"] + "_uss.feature"
    # Return the response value
    return response
