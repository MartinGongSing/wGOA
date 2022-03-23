
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
import requests
import math
from datetime import datetime
import time
from .models import cpc, instrument, cpc2, neph2, aps, psap
from django.db.models import Count, Q
import json

from .forms import ContactForm
################ camera START
from django.http.response import StreamingHttpResponse
from .camera import IPWebCam
# Create your views here.



def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def webcam_feed(request):
	return StreamingHttpResponse(gen(IPWebCam()),
					content_type='multipart/x-mixed-replace; boundary=frame')
################ camera END

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

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'success.html')

    form = ContactForm()
    context = {'form': form, 'segment': 'contact'}

    return render(request, 'contact.html', context)

    # return HttpResponse(html_template.render(context, request))


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


        data = {'ID': [], 'N': [], 'daycpc': [],
                'IDneph': [], 'sblue': [], 'sred' : [], 'sgreen': [],'bsblue': [], 'bsred' : [], 'bsgreen': [], 'dayneph': [],
                'IDaps': [], 'd1': [],'d2': [], 'd3': [], 'd4': [],'d5': [],'d6': [],'d7': [],'d8': [],'d9': [],'d10': [], 'dayaps': [], 'd11': [],'d12': [], 'd13': [], 'd14': [],'d15': [],'d16': [],'d17': [],'d18': [],'d19': [],
                'IDpsap': [], 'pblue': [], 'pred': [], 'pgreen': [], 'daypsap': [],
                }

        ###################
        ##### CPC_UBI #####
        ###################

        # valves = cpc2.objects.all() # we take all the items
        valves = cpc2.objects.order_by('ID')[:40]  # we take only 40 items

        for unit in valves:
            data['ID'].append(datetime.fromtimestamp(unit.ID/1000).strftime("%H:%M:%S")) #change the timestamp
            data['daycpc'].append(datetime.fromtimestamp(unit.ID/1000).strftime("%Y/%m/%d"))
            data['N'].append(unit.N)

        ####################
        ##### Neph_UBI #####
        ####################

        nephes = neph2.objects.order_by('ID')[:20]



        for unity in nephes:

            data['IDneph'].append(datetime.fromtimestamp(unity.ID/1000).strftime( "%H:%M:%S"))
            data['dayneph'].append(datetime.fromtimestamp(unit.ID / 1000).strftime("%Y/%m/%d"))
            data['sblue'].append(unity.sblue)
            data['sred'].append(unity.sred)
            data['sgreen'].append(unity.sgreen)
            data['bsblue'].append(unity.bsblue)
            data['bsred'].append(unity.bsred)
            data['bsgreen'].append(unity.bsgreen)

        #
        # print(testTime)
        ####################
        ##### PSAP_UBI #####
        ####################

        psapes = psap.objects.order_by('ID')[:20]

        for unites in psapes:
            data['IDpsap'].append(datetime.fromtimestamp(unites.ID/1000).strftime( "%H:%M:%S"))
            data['daypsap'].append(datetime.fromtimestamp(unit.ID / 1000).strftime("%Y/%m/%d"))
            data['pblue'].append(unites.blue)
            data['pred'].append(unites.red)
            data['pgreen'].append(unites.green)



        ###################
        ##### APS_UBI #####
        ###################


        apses = aps.objects.order_by('ID')[:40]

        upperLimit = 600

        for unita in apses:
            data['IDaps'].append(datetime.fromtimestamp(unita.ID/1000).strftime( "%H:%M:%S"))
            data['dayaps'].append(datetime.fromtimestamp(unit.ID / 1000).strftime("%Y/%m/%d"))
            data['d1'].append(isGreaterThan(unita.d1,upperLimit))
            data['d2'].append(isGreaterThan(unita.d2,upperLimit))
            data['d3'].append(isGreaterThan(unita.d3,upperLimit))
            data['d4'].append(isGreaterThan(unita.d4,upperLimit))
            data['d5'].append(isGreaterThan(unita.d5,upperLimit))
            data['d6'].append(isGreaterThan(unita.d6,upperLimit))
            data['d7'].append(isGreaterThan(unita.d7,upperLimit))
            data['d8'].append(isGreaterThan(unita.d8,upperLimit))
            data['d9'].append(isGreaterThan(unita.d9,upperLimit))
            data['d10'].append(isGreaterThan(unita.d10,upperLimit))
            data['d11'].append(isGreaterThan(unita.d11, upperLimit))
            data['d12'].append(isGreaterThan(unita.d12, upperLimit))
            data['d13'].append(isGreaterThan(unita.d13, upperLimit))
            data['d14'].append(isGreaterThan(unita.d14, upperLimit))
            data['d15'].append(isGreaterThan(unita.d15, upperLimit))
            data['d16'].append(isGreaterThan(unita.d16, upperLimit))
            data['d17'].append(isGreaterThan(unita.d17, upperLimit))
            data['d18'].append(isGreaterThan(unita.d18, upperLimit))
            data['d19'].append(isGreaterThan(unita.d19, upperLimit))


        return data

def isGreaterThan(x,y):
    if x>y:
        x = y
    else :
        x = x

    return x

def plot(request, chartID = 'chart_ID', chart_type = 'line', chart_height = 500,
         chartIDNeph = "chartIDNeph", chart_type_neph = 'line',
         chartIDAps = "chartIDAps", chart_type_aps = 'line',
         chartIDPsap = "chartIDPsap", chart_type_psap = 'line',
         ):

    data = ChartData.check_valve_data()

    ###################
    ##### CPC_UBI #####
    ###################

    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    title = {"text": 'CPC UBI '}
    xAxis = {"title": {"text": 'Time'}, "categories": data['ID']}
    yAxis = {"title": {"text": 'N/#/cm3'}}
    series = [
        {"name": 'N/#/cm3', "data": data['N'], "color":"#333fff"},
        ]
    daycpc = data["daycpc"][0] + " - " + data["daycpc"][-1]

    ####################
    ##### Neph_UBI #####
    ####################

    chartNeph = {"renderTo": chartIDNeph, "type": chart_type_neph, "height": chart_height, }
    titleNeph = {"text": 'Neph UBI'}
    xAxisNeph = {"title": {"text": 'Time'}, "categories": data['IDneph']}
    yAxisNeph = [{"title": {"text": '/\ σ<sub>s,bs</sub>/Mm<sup>-1</sup>'}, },{"title": {"text": 'o σ<sub>s,bs</sub>/Mm<sup>-1</sup>'},"opposite": "true"}] #TODO : Opposite axis
    seriesNeph = [
        {"name": 'Blue',     "yAxis": 0,  "data": data['sblue'],   "color":"#333fff",    "marker": {"symbol": "triangle"}  },
        {"name": 'Red',      "yAxis": 0,  "data": data['sred'],    "color":"#ff3333",    "marker": {"symbol": "triangle"}    },
        {"name": 'Green',    "yAxis": 0,  "data": data['sgreen'],  "color":"#33ff49",    "marker": {"symbol": "triangle"}    },
        {"name": 'bigBlue',  "yAxis": 1,  "data": data['bsblue'],  "color":"#8286ff",    "marker": {"symbol": "circle"}  },
        {"name": 'bigRed',   "yAxis": 1,  "data": data['bsred'],   "color":"#ff6e6e",    "marker": {"symbol": "circle"}    },
        {"name": 'bigGreen', "yAxis": 1,  "data": data['bsgreen'], "color":"#81de8b",    "marker": {"symbol": "circle"}    },
    ]
    dayneph = data["dayneph"][0] + " - " + data["dayneph"][-1]

    ####################
    ##### PSAP_UBI #####
    ####################

    chartPsap = {"renderTo": chartIDPsap, "type": chart_type_psap, "height": chart_height, }
    titlePsap = {"text": 'PSAP UBI'}
    xAxisPsap = {"title": {"text": 'Time'}, "categories": data['IDpsap']}
    yAxisPsap = [{"title": {"text": 'σ<sub>a</sub>/Mm<sup>-1</sup>'}}]
    seriesPsap = [
        {"name": 'Blue', "data": data['pblue'], "color": "#333fff"},
        {"name": 'Red', "data": data['pred'], "color": "#ff3333"},
        {"name": 'Green', "data": data['pgreen'], "color": "#33ff49"},

    ]
    daypsap = data["daypsap"][0] + " - " + data["daypsap"][-1]




    ###################
    ##### APS_UBI #####
    ###################
    chartAps = {"type": chart_type_aps,
        "marginTop": 40,
        "marginBottom": 80,
        "plotBorderWidth": 1,
        "renderTo": chartIDAps,  "height": chart_height, }
    chartAps2 = {"type": "heatmap",
                "marginTop": 40,
                "marginBottom": 80,
                "plotBorderWidth": 1,
                "renderTo": chartIDAps, "height": chart_height, }
    titleAps = {"text": 'APS UBI'}
    xAxisAps= {"categories": data['IDaps'],}
    yAxisAps= {
        "categories": ['d1','d2','d3','d4','d5','d6','d7','d8','d9','d10'], #'type': 'logarithmic', #precise logarithmic scale define upper limit    ,'d11','d12','d13','d14','d15','d16','d17','d18','d19'
    }
    dayaps = data["dayaps"][0] + " - " + data["dayaps"][-1]

    vd1 = data['d1'][20]
    vd2 = data['d2'][20]
    vd3 = data['d3'][20]
    vd4 = data['d4'][20]
    vd5 = data['d5'][20]
    vd6 = data['d6'][20]
    vd7 = data['d7'][20]
    vd8 = data['d8'][20]
    vd9 = data['d9'][20]
    vd10 = data['d10'][20]

    vd11 = data['d1'][21]
    vd12 = data['d2'][21]
    vd13 = data['d3'][21]
    vd14 = data['d4'][21]
    vd15 = data['d5'][21]
    vd16 = data['d6'][21]
    vd17 = data['d7'][21]
    vd18 = data['d8'][21]
    vd19 = data['d9'][21]
    vd20 = data['d10'][21]

    vd21 = data['d1'][22]
    vd22 = data['d2'][22]
    vd23 = data['d3'][22]
    vd24 = data['d4'][22]
    vd25 = data['d5'][22]
    vd26 = data['d6'][22]
    vd27 = data['d7'][22]
    vd28 = data['d8'][22]
    vd29 = data['d9'][22]
    vd30 = data['d10'][22]

    vd31 = data['d1'][23]
    vd32 = data['d2'][23]
    vd33 = data['d3'][23]
    vd34 = data['d4'][23]
    vd35 = data['d5'][23]
    vd36 = data['d6'][23]
    vd37 = data['d7'][23]
    vd38 = data['d8'][23]
    vd39 = data['d9'][23]
    vd40 = data['d10'][23]

    vd41 = data['d1'][24]
    vd42 = data['d2'][24]
    vd43 = data['d3'][24]
    vd44 = data['d4'][24]
    vd45 = data['d5'][24]
    vd46 = data['d6'][24]
    vd47 = data['d7'][24]
    vd48 = data['d8'][24]
    vd49 = data['d9'][24]
    vd50 = data['d10'][24]

    vd51 = data['d1'][25]
    vd52 = data['d2'][25]
    vd53 = data['d3'][25]
    vd54 = data['d4'][25]
    vd55 = data['d5'][25]
    vd56 = data['d6'][25]
    vd57 = data['d7'][25]
    vd58 = data['d8'][25]
    vd59 = data['d9'][25]
    vd60 = data['d10'][25]

    vd61 = data['d1'][26]
    vd62 = data['d2'][26]
    vd63 = data['d3'][26]
    vd64 = data['d4'][26]
    vd65 = data['d5'][26]
    vd66 = data['d6'][26]
    vd67 = data['d7'][26]
    vd68 = data['d8'][26]
    vd69 = data['d9'][26]



    #############################

    # v1d1 = data['d11'][20]
    # v1d2 = data['d12'][20]
    # v1d3 = data['d13'][20]
    # v1d4 = data['d14'][20]
    # v1d5 = data['d15'][20]
    # v1d6 = data['d16'][20]
    # v1d7 = data['d17'][20]
    # v1d8 = data['d18'][20]
    # v1d9 = data['d19'][20]
    # v1d10 = data['d10'][20]
    # v1d11 = data['d11'][21]
    # v1d12 = data['d12'][21]
    # v1d13 = data['d13'][21]
    # v1d14 = data['d14'][21]
    # v1d15 = data['d15'][21]
    # v1d16 = data['d16'][21]
    # v1d17 = data['d17'][21]
    # v1d18 = data['d18'][21]
    # v1d19 = data['d19'][21]
    # v1d20 = data['d10'][21]
    # v1d21 = data['d11'][22]
    # v1d22 = data['d12'][22]
    # v1d23 = data['d13'][22]
    # v1d24 = data['d14'][22]
    # v1d25 = data['d15'][22]
    # v1d26 = data['d16'][22]
    # v1d27 = data['d17'][22]
    # v1d28 = data['d18'][22]
    # v1d29 = data['d19'][22]
    # v1d30 = data['d10'][22]
    # v1d31 = data['d11'][23]
    # v1d32 = data['d12'][23]
    # v1d33 = data['d13'][23]
    # v1d34 = data['d14'][23]
    # v1d35 = data['d15'][23]
    # v1d36 = data['d16'][23]
    # v1d37 = data['d17'][23]
    # v1d38 = data['d18'][23]
    # v1d39 = data['d19'][23]
    # v1d40 = data['d10'][23]
    # v1d41 = data['d11'][24]
    # v1d42 = data['d12'][24]
    # v1d43 = data['d13'][24]
    # v1d44 = data['d14'][24]
    # v1d45 = data['d15'][24]
    # v1d46 = data['d16'][24]
    # v1d47 = data['d17'][24]
    # v1d48 = data['d18'][24]
    # v1d49 = data['d19'][24]
    # v1d50 = data['d10'][24]
    # v1d51 = data['d11'][25]
    # v1d52 = data['d12'][25]
    # v1d53 = data['d13'][25]
    # v1d54 = data['d14'][25]
    # v1d55 = data['d15'][25]
    # v1d56 = data['d16'][25]
    # v1d57 = data['d17'][25]
    # v1d58 = data['d18'][25]
    # v1d59 = data['d19'][25]
    # v1d60 = data['d10'][25]
    # v1d61 = data['d11'][26]
    # v1d62 = data['d12'][26]
    # v1d63 = data['d13'][26]
    # v1d64 = data['d14'][26]
    # v1d65 = data['d15'][26]
    # v1d66 = data['d16'][26]
    # v1d67 = data['d17'][26]
    # v1d68 = data['d18'][26]
    # v1d69 = data['d19'][26]



    ############################


    seriesAps = [
        {"name": 'd1', "data": data['d1'], "color": "#333fff"},
        {"name": 'd2', "data": data['d2'], "color": "#ff3333"},
        {"name": 'd3', "data": data['d3'], "color": "#33ff49"},
        {"name": 'd4', "data": data['d4'], "color": "#333fff"},
        {"name": 'd5', "data": data['d5'], "color": "#ff3333"},
        {"name": 'd6', "data": data['d6'], "color": "#33ff49"},

    ]


        #

        # [0, 0, 10], [0, 1, 19], [0, 2, 8], [0, 3, 24], [0, 4, 67], [1, 0, 92], [1, 1, 58], [1, 2, 78], [1, 3, 117], [1, 4, 48], [2, 0, 35], [2, 1, 15], [2, 2, 123], [2, 3, 64], [2, 4, 52], [3, 0, 72], [3, 1, 132], [3, 2, 114], [3, 3, 19], [3, 4, 16], [4, 0, 38], [4, 1, 5], [4, 2, 8], [4, 3, 117], [4, 4, 115], [5, 0, 88], [5, 1, 32], [5, 2, 12], [5, 3, 6], [5, 4, 120], [6, 0, 13], [6, 1, 44], [6, 2, 88], [6, 3, 98], [6, 4, 96], [7, 0, 31], [7, 1, 1], [7, 2, 82], [7, 3, 32], [7, 4, 30], [8, 0, 85], [8, 1, 97], [8, 2, 123], [8, 3, 64], [8, 4, 84], [9, 0, 47], [9, 1, 114], [9, 2, 31], [9, 3, 48], [9, 4, 91]],
        #          "dataLabels": {
        #
        #              "color": '#000000'
        #          }







    return render(request, 'data3.html', {
                                        'chartID': chartID,
                                        'chart': chart,
                                        'series': series,
                                        'title': title,
                                        'xAxis': xAxis,
                                        'yAxis': yAxis,
                                        'daycpc':daycpc,

                                        'chartIDNeph': chartIDNeph,
                                        'chartNeph' : chartNeph ,
                                        'titleNeph' : titleNeph ,
                                        'xAxisNeph' : xAxisNeph ,
                                        'yAxisNeph' : yAxisNeph ,
                                        'seriesNeph' : seriesNeph,
                                        'dayneph': dayneph,

                                        "chartIDPsap" : chartIDPsap,
                                        "chartPsap": chartPsap,
                                        "titlePsap" : titlePsap,
                                        "xAxisPsap" : xAxisPsap,
                                        "yAxisPsap" : yAxisPsap,
                                        "seriesPsap" : seriesPsap,
                                        "daypsap" : daypsap,

                                        'chartIDAps': chartIDAps,
                                        'chartAps': chartAps,
                                        'chartAps2': chartAps2,
                                        'titleAps': titleAps,
                                        'xAxisAps': xAxisAps,
                                        'yAxisAps': yAxisAps,
                                        'seriesAps': seriesAps,
                                        'dayaps' : dayaps,

                                        'vd1': vd1,
                                        'vd2': vd2,
                                        'vd3': vd3,
                                        'vd4': vd4,
                                        'vd5': vd5,
                                        'vd6': vd6,
                                        'vd7': vd7,
                                        'vd8': vd8,
                                        'vd9': vd9,
                                        'vd10': vd10,

                                        'vd11': vd11,
                                        'vd12': vd12,
                                        'vd13': vd13,
                                        'vd14': vd14,
                                        'vd15': vd15,
                                        'vd16': vd16,
                                        'vd17': vd17,
                                        'vd18': vd18,
                                        'vd19': vd19,
                                        'vd20': vd20,

                                        'vd21': vd21,
                                        'vd22': vd22,
                                        'vd23': vd23,
                                        'vd24': vd24,
                                        'vd25': vd25,
                                        'vd26': vd26,
                                        'vd27': vd27,
                                        'vd28': vd28,
                                        'vd29': vd29,
                                        'vd30': vd30,

                                        'vd31': vd31,
                                        'vd32': vd32,
                                        'vd33': vd33,
                                        'vd34': vd34,
                                        'vd35': vd35,
                                        'vd36': vd36,
                                        'vd37': vd37,
                                        'vd38': vd38,
                                        'vd39': vd39,
                                        'vd40': vd40,

                                        'vd41': vd41,
                                        'vd42': vd42,
                                        'vd43': vd43,
                                        'vd44': vd44,
                                        'vd45': vd45,
                                        'vd46': vd46,
                                        'vd47': vd47,
                                        'vd48': vd48,
                                        'vd49': vd49,
                                        'vd50': vd50,

                                        'vd51': vd51,
                                        'vd52': vd52,
                                        'vd53': vd53,
                                        'vd54': vd54,
                                        'vd55': vd55,
                                        'vd56': vd56,
                                        'vd57': vd57,
                                        'vd58': vd58,
                                        'vd59': vd59,
                                        'vd60': vd60,

                                        'vd61': vd61,
                                        'vd62': vd62,
                                        'vd63': vd63,
                                        'vd64': vd64,
                                        'vd65': vd65,
                                        'vd66': vd66,
                                        'vd67': vd67,
                                        'vd68': vd68,
                                        'vd69': vd69,

        # 'v1d1': v1d1,
        # 'v1d2': v1d2,
        # 'v1d3': v1d3,
        # 'v1d4': v1d4,
        # 'v1d5': v1d5,
        # 'v1d6': v1d6,
        # 'v1d7': v1d7,
        # 'v1d8': v1d8,
        # 'v1d9': v1d9,
        # 'v1d10': v1d10,
        # 'v1d11': v1d11,
        # 'v1d12': v1d12,
        # 'v1d13': v1d13,
        # 'v1d14': v1d14,
        # 'v1d15': v1d15,
        # 'v1d16': v1d16,
        # 'v1d17': v1d17,
        # 'v1d18': v1d18,
        # 'v1d19': v1d19,
        # 'v1d20': v1d20,
        # 'v1d21': v1d21,
        # 'v1d22': v1d22,
        # 'v1d23': v1d23,
        # 'v1d24': v1d24,
        # 'v1d25': v1d25,
        # 'v1d26': v1d26,
        # 'v1d27': v1d27,
        # 'v1d28': v1d28,
        # 'v1d29': v1d29,
        # 'v1d30': v1d30,
        # 'v1d31': v1d31,
        # 'v1d32': v1d32,
        # 'v1d33': v1d33,
        # 'v1d34': v1d34,
        # 'v1d35': v1d35,
        # 'v1d36': v1d36,
        # 'v1d37': v1d37,
        # 'v1d38': v1d38,
        # 'v1d39': v1d39,
        # 'v1d40': v1d40,
        # 'v1d41': v1d41,
        # 'v1d42': v1d42,
        # 'v1d43': v1d43,
        # 'v1d44': v1d44,
        # 'v1d45': v1d45,
        # 'v1d46': v1d46,
        # 'v1d47': v1d47,
        # 'v1d48': v1d48,
        # 'v1d49': v1d49,
        # 'v1d50': v1d50,
        # 'v1d51': v1d51,
        # 'v1d52': v1d52,
        # 'v1d53': v1d53,
        # 'v1d54': v1d54,
        # 'v1d55': v1d55,
        # 'v1d56': v1d56,
        # 'v1d57': v1d57,
        # 'v1d58': v1d58,
        # 'v1d59': v1d59,
        # 'v1d60': v1d60,
        # 'v1d61': v1d61,
        # 'v1d62': v1d62,
        # 'v1d63': v1d63,
        # 'v1d64': v1d64,
        # 'v1d65': v1d65,
        # 'v1d66': v1d66,
        # 'v1d67': v1d67,
        # 'v1d68': v1d68,
        # 'v1d69': v1d69,

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

