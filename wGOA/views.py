
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
import requests
import math
from .models import cpc, instrument, cpc2, neph2
from django.db.models import Count, Q


def index(request):
    # return HttpResponse("Hello world ! ")
    context = {'segment': 'index'}

    html_template = loader.get_template('index.html')

    ################
    # start WEATHER
    ################

    city_name = "Covilha"
    api_key = "79cba0dd8efda8493fa45cbb9c734a40"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}"
    w_dataset = requests.get(url).json()

    try:
        context = {
            ####
            "city_name": w_dataset["city"]["name"],
            "city_country": w_dataset["city"]["country"],
            "wind": w_dataset['list'][0]['wind']['speed'],
            "degree": w_dataset['list'][0]['wind']['deg'],
            "status": w_dataset['list'][0]['weather'][0]['description'],
            "cloud": w_dataset['list'][0]['clouds']['all'],
            'date': w_dataset['list'][0]["dt_txt"],
            'date1': w_dataset['list'][1]["dt_txt"],
            'date2': w_dataset['list'][2]["dt_txt"],
            'date3': w_dataset['list'][3]["dt_txt"],
            'date4': w_dataset['list'][4]["dt_txt"],
            'date5': w_dataset['list'][5]["dt_txt"],
            'date6': w_dataset['list'][6]["dt_txt"],

            "temp": round(w_dataset["list"][0]["main"]["temp"] - 273.0),
            "temp_min1": math.floor(w_dataset["list"][1]["main"]["temp_min"] - 273.0),
            "temp_max1": math.ceil(w_dataset["list"][1]["main"]["temp_max"] - 273.0),
            "temp_min2": math.floor(w_dataset["list"][2]["main"]["temp_min"] - 273.0),
            "temp_max2": math.ceil(w_dataset["list"][2]["main"]["temp_max"] - 273.0),
            "temp_min3": math.floor(w_dataset["list"][3]["main"]["temp_min"] - 273.0),
            "temp_max3": math.ceil(w_dataset["list"][3]["main"]["temp_max"] - 273.0),
            "temp_min4": math.floor(w_dataset["list"][4]["main"]["temp_min"] - 273.0),
            "temp_max4": math.ceil(w_dataset["list"][4]["main"]["temp_max"] - 273.0),
            "temp_min5": math.floor(w_dataset["list"][5]["main"]["temp_min"] - 273.0),
            "temp_max5": math.ceil(w_dataset["list"][5]["main"]["temp_max"] - 273.0),
            "temp_min6": math.floor(w_dataset["list"][6]["main"]["temp_min"] - 273.0),
            "temp_max6": math.ceil(w_dataset["list"][6]["main"]["temp_max"] - 273.0),

            "pressure": w_dataset["list"][0]["main"]["pressure"],
            "humidity": w_dataset["list"][0]["main"]["humidity"],
            "sea_level": w_dataset["list"][0]["main"]["sea_level"],

            "weather": w_dataset["list"][1]["weather"][0]["main"],
            "description": w_dataset["list"][1]["weather"][0]["description"],
            "icon": w_dataset["list"][0]["weather"][0]["icon"],
            "icon1": w_dataset["list"][1]["weather"][0]["icon"],
            "icon2": w_dataset["list"][2]["weather"][0]["icon"],
            "icon3": w_dataset["list"][3]["weather"][0]["icon"],
            "icon4": w_dataset["list"][4]["weather"][0]["icon"],
            "icon5": w_dataset["list"][5]["weather"][0]["icon"],
            "icon6": w_dataset["list"][6]["weather"][0]["icon"],

        }
    except:
        context = {

            "city_name": "Not Found, Check your spelling..."
        }

    ##############
    # END WEATHER
    ##############



    return HttpResponse(html_template.render(context, request))

def station(request):
    # return HttpResponse("this is the weather station page")
    context = {'segment': 'station'}

    html_template = loader.get_template('station.html')
    return HttpResponse(html_template.render(context, request))

def intranet(request):

    context = {'segment': 'intranet'}

    html_template = loader.get_template('intranet.html')
    return HttpResponse(html_template.render(context, request))

def contact(request):
    #return HttpResponse("this is the contact page")
    context = {'segment': 'contact'}

    html_template = loader.get_template('contact.html')
    return HttpResponse(html_template.render(context, request))


############### INSTRUMENTS PAGES ###############
def instruments(request):
    instrums = instrument.objects.all()

    return render(request, 'instruments.html', {'instrums': instrums} )

def dyna_instrum(request, id):
    obj = instrument.objects.get(id=id)
    context = {
        "instrum" : obj
    }
    return render(request, '../templates/instrum_detail.html', context)



############### DATA PAGES ###############

def data1(request):
    # resultdisplay = cpc.objects.all()

    resultdisplay = neph2.objects.order_by('ID')[:10] #Just to get the X lasts elements of the list
    cpcdisplay = cpc2.objects.order_by('ID')[:10]
    return render(request, "data.html", {'neph2': resultdisplay, 'cpc2': cpcdisplay})

def data2(request):
    # resultdisplay = cpc2.objects.order_by('ID')[:10] #Just to get the X lasts elements of the list
    #
    # return render(request, "data2.html", {'cpc2': resultdisplay})
    dataset = cpc.objects.order_by('Time')[:10]
    # dataset = cpc2.objects \
    #     .values('N') \
    #     .order_by('ID')
    return render(request, 'data2.html', {'dataset': dataset})

########### Graphs     https://stackoverflow.com/questions/27810087/passing-django-database-queryset-to-highcharts-via-json
class ChartData(object):
    def check_valve_data():


        data = {'ID': [], 'N': [],
                'IDneph': [], 'sblue': [], 'sred' : [], 'sgreen': [],'bsblue': [], 'bsred' : [], 'bsgreen': [],

                }

        ###################
        ##### CPC_UBI #####
        ###################

        # valves = cpc2.objects.all()
        valves = cpc2.objects.order_by('ID')[:40]

        for unit in valves:
            data['ID'].append(unit.ID)
            data['N'].append(unit.N)

        ####################
        ##### Neph_UBI #####
        ####################

        nephes = neph2.objects.order_by('ID')[:40]

        for unity in nephes:
            data['IDneph'].append(unity.ID)
            data['sblue'].append(unity.sblue)
            data['sred'].append(unity.sred)
            data['sgreen'].append(unity.sgreen)
            # data['bsblue'].append(unity.bsblue)
            # data['bsred'].append(unity.bsred)
            # data['bsgreen'].append(unity.bsgreen)


        return data

def plot(request, chartID = 'chart_ID', chart_type = 'line', chart_height = 500, chartIDNeph = "chartIDNeph", chart_type_neph = 'line' ):

    data = ChartData.check_valve_data()

    ###################
    ##### CPC_UBI #####
    ###################

    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    title = {"text": 'CPC UBI'}
    xAxis = {"title": {"text": 'Time'}, "categories": data['ID']}
    yAxis = {"title": {"text": 'Data'}}
    series = [
        {"name": 'N/#/cm3', "data": data['N']},
        ]

    ####################
    ##### Neph_UBI #####
    ####################

    chartNeph = {"renderTo": chartIDNeph, "type": chart_type_neph, "height": chart_height, }
    titleNeph = {"text": 'Neph UBI'}
    xAxisNeph = {"title": {"text": 'Time'}, "categories": data['IDneph']}
    yAxisNeph = {"title": {"text": 'Data'}}
    seriesNeph = [
        {"name": 'Blue', "data": data['sblue']},
    ]


    return render(request, 'data2.html', {
                                        'chartID': chartID,
                                        'chart': chart,
                                        'series': series,
                                        'title': title,
                                        'xAxis': xAxis,
                                        'yAxis': yAxis,

                                        'chartIDNeph': chartIDNeph,
                                        'chartNeph' : chartNeph ,
                                        'titleNeph' : titleNeph ,
                                        'xAxisNeph' : xAxisNeph ,
                                        'yAxisNeph' : yAxisNeph ,
                                        'seriesNeph' : seriesNeph,
                                          })


############### TEST ###############


# def filt(ListView):
#     model: instrument
#     template_name = 'instrum_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['filter']=instrumFilter(self.request.GET, queryset=self.get_queryset())
#         return context
#
# def search(request):
#     instrum_list = instrument.objects.all()
#     instrum_filter = instrumFilter(request, queryset=instrum_list)
#     return render(request, 'instrum_detail.html', {'filter': instrum_filter})




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


# def data(request):
#     # return HttpResponse("this is the data page")
#     context = {'segment': 'data'}
#     # resultdisplay = CPC.objects.all()
#     html_template = loader.get_template('data.html')
#     return HttpResponse(html_template.render(context, request, {'CPC': resultdisplay})) #, {'CPC': resultdisplay}

