
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse


def index(request):
    # return HttpResponse("Hello world ! ")
    context = {'segment': 'index'}

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


def instruments(request):
    return HttpResponse("this is the instrument page")