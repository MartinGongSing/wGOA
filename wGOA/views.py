
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
import requests
import math
from .models import cpc, instrument, cpc2, neph2, aps, psap
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
    psapdisplay = psap.objects.order_by('ID')[:10]
    apsdisplay = aps.objects.order_by('ID')[:10]
    return render(request, "data.html", {'neph2': resultdisplay, 'cpc2': cpcdisplay, 'aps' : apsdisplay, 'psap' : psapdisplay})

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
                'IDaps': [], 'd1': [],'d2': [], 'd3': [], 'd4': [],'d5': [],'d6': [],'d7': [],'d8': [],'d9': [],'d10': [],
                'IDpsap': [], 'pblue': [], 'pred': [], 'pgreen': [],
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
            data['bsblue'].append(unity.bsblue)
            data['bsred'].append(unity.bsred)
            data['bsgreen'].append(unity.bsgreen)

        ####################
        ##### PSAP_UBI #####
        ####################

        psapes = psap.objects.order_by('ID')[:40]

        for unites in psapes:
            data['IDpsap'].append(unites.ID)
            data['pblue'].append(unites.blue)
            data['pred'].append(unites.red)
            data['pgreen'].append(unites.green)


        ###################
        ##### APS_UBI #####
        ###################


        apses = aps.objects.order_by('ID')[:40]

        for unita in apses:
            data['IDaps'].append(unita.ID)
            data['d1'].append(unita.d1)
            data['d2'].append(unita.d2)
            data['d3'].append(unita.d3)
            data['d4'].append(unita.d4)
            data['d5'].append(unita.d5)
            data['d6'].append(unita.d6)
            data['d7'].append(unita.d7)
            data['d8'].append(unita.d8)
            data['d9'].append(unita.d9)
            data['d10'].append(unita.d10)


        return data

def plot(request, chartID = 'chart_ID', chart_type = 'line', chart_height = 500,
         chartIDNeph = "chartIDNeph", chart_type_neph = 'line',
         chartIDAps = "chartIDAps", chart_type_aps = 'heatmap',
         chartIDPsap = "chartIDPsap", chart_type_psap = 'line',
         ):

    data = ChartData.check_valve_data()

    ###################
    ##### CPC_UBI #####
    ###################

    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    title = {"text": 'CPC UBI'}
    xAxis = {"title": {"text": 'Time'}, "categories": data['ID']}
    yAxis = {"title": {"text": 'N/#/cm3'}}
    series = [
        {"name": 'N/#/cm3', "data": data['N'], "color":"#333fff"},
        ]

    ####################
    ##### Neph_UBI #####
    ####################

    chartNeph = {"renderTo": chartIDNeph, "type": chart_type_neph, "height": chart_height, }
    titleNeph = {"text": 'Neph UBI'}
    xAxisNeph = {"title": {"text": 'Time'}, "categories": data['IDneph']}
    yAxisNeph = [{"title": {"text": 'bs/Mm-1'}}] #TODO : Opposite axis
    seriesNeph = [
        {"name": 'Blue', "data": data['sblue'], "color":"#333fff"},
        {"name": 'Red', "data": data['sred'],"color":"#ff3333"},
        {"name": 'Green', "data": data['sgreen'],"color":"#33ff49"},
        {"name": 'bigBlue', "data": data['bsblue'],"color":"#33fff6"},
        {"name": 'bigRed', "data": data['bsred'],"color":"#ff33ca"},
        {"name": 'bigGreen', "data": data['bsgreen'],"color":"#a2ff33"},
    ]

    ####################
    ##### PSAP_UBI #####
    ####################

    chartPsap = {"renderTo": chartIDPsap, "type": chart_type_psap, "height": chart_height, }
    titlePsap = {"text": 'PSAP UBI'}
    xAxisPsap = {"title": {"text": 'Time'}, "categories": data['IDpsap']}
    yAxisPsap = [{"title": {"text": 'σa/Mm-1'}}]
    seriesPsap = [
        {"name": 'Blue', "data": data['pblue'], "color": "#333fff"},
        {"name": 'Red', "data": data['pred'], "color": "#ff3333"},
        {"name": 'Green', "data": data['pgreen'], "color": "#33ff49"},

    ]



    ###################
    ##### APS_UBI #####
    ###################
    chartAps = {"renderTo": chartIDAps, "type": chart_type_aps, "height": chart_height, }
    titleAps = {"text": 'APS UBI'}
    xAxisAps= {"categories": data['IDaps']}
    yAxisAps= {
    "categories": ['d1','d2','d3','d4','d5','d6','d7','d8','d9','d10']
    }

    seriesAps = {"name": 'test', "data": [[0, 0, 10], [0, 1, 19], [0, 2, 8], [0, 3, 24], [0, 4, 67], [1, 0, 92], [1, 1, 58], [1, 2, 78], [1, 3, 117], [1, 4, 48], [2, 0, 35], [2, 1, 15], [2, 2, 123], [2, 3, 64], [2, 4, 52], [3, 0, 72], [3, 1, 132], [3, 2, 114], [3, 3, 19], [3, 4, 16], [4, 0, 38], [4, 1, 5], [4, 2, 8], [4, 3, 117], [4, 4, 115], [5, 0, 88], [5, 1, 32], [5, 2, 12], [5, 3, 6], [5, 4, 120], [6, 0, 13], [6, 1, 44], [6, 2, 88], [6, 3, 98], [6, 4, 96], [7, 0, 31], [7, 1, 1], [7, 2, 82], [7, 3, 32], [7, 4, 30], [8, 0, 85], [8, 1, 97], [8, 2, 123], [8, 3, 64], [8, 4, 84], [9, 0, 47], [9, 1, 114], [9, 2, 31], [9, 3, 48], [9, 4, 91]],
                 "dataLabels": {

                     "color": '#000000'
                 }
                 }





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

                                        'chartIDAps': chartIDAps,
                                        'chartAps': chartAps,
                                        'titleAps': titleAps,
                                        'xAxisAps': xAxisAps,
                                        'yAxisAps': yAxisAps,
                                        'seriesAps': seriesAps,

                                        "chartIDPsap" : chartIDPsap,
                                        "chartPsap": chartPsap,
                                        "titlePsap" : titlePsap,
                                        "xAxisPsap" : xAxisPsap,
                                        "yAxisPsap" : yAxisPsap,
                                        "seriesPsap" : seriesPsap,
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

