
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

def data(request):
    # return HttpResponse("this is the data page")
    context = {'segment': 'data'}

    html_template = loader.get_template('data.html')
    return HttpResponse(html_template.render(context, request))

def instruments(request):
    # return HttpResponse("this is the instrument page")
    context = {'segment': 'instruments'}

    html_template = loader.get_template('instruments.html')
    return HttpResponse(html_template.render(context, request))

def station(request):
    # return HttpResponse("this is the weather station page")
    context = {'segment': 'station'}

    html_template = loader.get_template('station.html')
    return HttpResponse(html_template.render(context, request))

def intranet(request):
    # return HttpResponse("this is the intranet page")
    context = {'segment': 'intranet'}

    html_template = loader.get_template('intranet.html')
    return HttpResponse(html_template.render(context, request))

def contact(request):
    #return HttpResponse("this is the contact page")
    context = {'segment': 'contact'}

    html_template = loader.get_template('contact.html')
    return HttpResponse(html_template.render(context, request))



def instrument1(request):
    # return HttpResponse("this is the instrument page")
    context = {'segment': 'instrument1'}

    html_template = loader.get_template('instruments/instrum1.html')
    return HttpResponse(html_template.render(context, request))


# def pages(request):
#     contex = {}
#
#     try:
#
#
#     except template.TemplateDoesNotExist:
#
#         html_template = loader.get_template('page-404.html')
#         return HttpResponse(html_template.render(context, request))
#
#     except:
#         html_template = loader.get_template('page-500.html')
#         return HttpResponse(html_template.render(context, request))
