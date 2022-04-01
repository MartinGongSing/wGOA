
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
from .models import cpc, instrument, cpc2, neph2, aps, psap, cpc3
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

def previous(request):

    context = {'segment': 'previous'}

    html_template = loader.get_template('previous.html')
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
    apsdisplay = aps.objects.order_by('time')[:10]
    return render(request, "data.html", {'neph2': resultdisplay, 'cpc2': cpcdisplay, 'aps' : apsdisplay, 'psap' : psapdisplay})

def data2(request):
    # resultdisplay = cpc2.objects.order_by('ID')[:10] #Just to get the X lasts elements of the list

    dataset = cpc.objects.order_by('Time')[:10]

    return render(request, 'data2.html', {'dataset': dataset})




########### Graphs     https://stackoverflow.com/questions/27810087/passing-django-database-queryset-to-highcharts-via-json
class ChartData(object):
    def check_the_data():


        data = {'ID': [], 'N': [], 'daycpc': [],
                'IDneph': [], 'sblue': [], 'sred' : [], 'sgreen': [],'bsblue': [], 'bsred' : [], 'bsgreen': [], 'dayneph': [],
                'IDaps': [], 'd1': [],'d2': [], 'd3': [], 'd4': [],'d5': [],'d6': [],'d7': [],'d8': [],'d9': [],'d10': [], 'dayaps': [], 'd11': [],'d12': [], 'd13': [], 'd14': [],'d15': [],'d16': [],'d17': [],'d18': [],'d19': [],'d20': [],'d21': [],'d22': [], 'd23': [], 'd24': [],'d25': [],'d26': [],'d27': [],'d28': [],'d29': [],'d30': [],'d31': [],'d32': [], 'd33': [], 'd34': [],'d35': [],'d36': [],'d37': [],'d38': [],'d39': [],'d40': [],'d41': [],'d42': [],'d43':[],
                'IDpsap': [], 'pblue': [], 'pred': [], 'pgreen': [], 'daypsap': [],
                }

        ###################
        ##### CPC_UBI #####
        ###################

        # cpces = cpc2.objects.all() # we take all the items
        # cpces = cpc2.objects.order_by('ID')[:288]  # we take only 40 items

        cpc3display = cpc3.objects.using('dataGOA').order_by('-time')[:288]
        print(type(cpc3display))

        for unit in cpc3display:
            data['ID'].insert(0,datetime.fromtimestamp(unit.time/1000).strftime("%H:%M")) #change the timestamp
            data['daycpc'].insert(0,datetime.fromtimestamp(unit.time/1000).strftime("%Y/%m/%d"))
            data['N'].insert(0,unit.N)






        ####################
        ##### Neph_UBI #####
        ####################
        nephes = neph2.objects.using('dataGOA').order_by('-time')[:1440]

        for unity in nephes:

            data['IDneph'].insert(0,datetime.fromtimestamp(unity.time/1000).strftime( "%H:%M"))
            data['dayneph'].insert(0,datetime.fromtimestamp(unity.time/ 1000).strftime("%Y/%m/%d"))
            data['sblue'].insert(0,unity.sblue * 1000000) # x 10^6
            data['sred'].insert(0,unity.sred * 1000000)
            data['sgreen'].insert(0,unity.sgreen * 1000000)
            data['bsblue'].insert(0,unity.bsblue * 1000000)
            data['bsred'].insert(0,unity.bsred * 1000000)
            data['bsgreen'].insert(0,unity.bsgreen * 1000000)


        ####################
        ##### PSAP_UBI #####
        ####################
        psapes = psap.objects.using('dataGOA').order_by('-time')[1:1440]

        for unites in psapes:
            data['IDpsap'].insert(0,datetime.fromtimestamp(unites.time/1000).strftime( "%H:%M"))
            data['daypsap'].insert(0,datetime.fromtimestamp(unites.time/ 1000).strftime("%Y/%m/%d"))
            data['pblue'].insert(0,unites.blue)
            data['pred'].insert(0,unites.red)
            data['pgreen'].insert(0,unites.green)



        ###################
        ##### APS_UBI #####
        ###################
        apses = aps.objects.using('dataGOA').order_by('-time')[:144]

        upperLimit = 600

        for unita in apses:
            data['IDaps'].insert(0,datetime.fromtimestamp(unita.time/1000).strftime( "%H:%M"))
            data['dayaps'].insert(0,datetime.fromtimestamp(unita.time/ 1000).strftime("%Y/%m/%d"))
            data['d1'].insert(0,isGreaterThan(unita.d1,upperLimit))
            data['d2'].insert(0,isGreaterThan(unita.d2,upperLimit))
            data['d3'].insert(0,isGreaterThan(unita.d3,upperLimit))
            data['d4'].insert(0,isGreaterThan(unita.d4,upperLimit))
            data['d5'].insert(0,isGreaterThan(unita.d5,upperLimit))
            data['d6'].insert(0,isGreaterThan(unita.d6,upperLimit))
            data['d7'].insert(0,isGreaterThan(unita.d7,upperLimit))
            data['d8'].insert(0,isGreaterThan(unita.d8,upperLimit))
            data['d9'].insert(0,isGreaterThan(unita.d9,upperLimit))
            data['d10'].insert(0,isGreaterThan(unita.d10,upperLimit))
            data['d11'].insert(0,isGreaterThan(unita.d11, upperLimit))
            data['d12'].insert(0,isGreaterThan(unita.d12, upperLimit))
            data['d13'].insert(0,isGreaterThan(unita.d13, upperLimit))
            data['d14'].insert(0,isGreaterThan(unita.d14, upperLimit))
            data['d15'].insert(0,isGreaterThan(unita.d15, upperLimit))
            data['d16'].insert(0,isGreaterThan(unita.d16, upperLimit))
            data['d17'].insert(0,isGreaterThan(unita.d17, upperLimit))
            data['d18'].insert(0,isGreaterThan(unita.d18, upperLimit))
            data['d19'].insert(0,isGreaterThan(unita.d19, upperLimit))
            data['d20'].insert(0,isGreaterThan(unita.d20, upperLimit))
            data['d21'].insert(0,isGreaterThan(unita.d21, upperLimit))
            data['d22'].insert(0,isGreaterThan(unita.d22, upperLimit))
            data['d23'].insert(0,isGreaterThan(unita.d23, upperLimit))
            data['d24'].insert(0,isGreaterThan(unita.d24, upperLimit))
            data['d25'].insert(0,isGreaterThan(unita.d25, upperLimit))
            data['d26'].insert(0,isGreaterThan(unita.d26, upperLimit))
            data['d27'].insert(0,isGreaterThan(unita.d27, upperLimit))
            data['d28'].insert(0,isGreaterThan(unita.d28, upperLimit))
            data['d29'].insert(0,isGreaterThan(unita.d29, upperLimit))
            data['d30'].insert(0,isGreaterThan(unita.d30, upperLimit))
            data['d31'].insert(0,isGreaterThan(unita.d31, upperLimit))
            data['d32'].insert(0,isGreaterThan(unita.d32, upperLimit))
            data['d33'].insert(0,isGreaterThan(unita.d33, upperLimit))
            data['d34'].insert(0,isGreaterThan(unita.d34, upperLimit))
            data['d35'].insert(0,isGreaterThan(unita.d35, upperLimit))
            data['d36'].insert(0,isGreaterThan(unita.d36, upperLimit))
            data['d37'].insert(0,isGreaterThan(unita.d37, upperLimit))
            data['d38'].insert(0,isGreaterThan(unita.d38, upperLimit))
            data['d39'].insert(0,isGreaterThan(unita.d39, upperLimit))
            data['d40'].insert(0,isGreaterThan(unita.d40, upperLimit))
            data['d41'].insert(0,isGreaterThan(unita.d41, upperLimit))
            data['d42'].insert(0,isGreaterThan(unita.d42, upperLimit))
            data['d43'].insert(0,isGreaterThan(unita.d43, upperLimit))

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

    data = ChartData.check_the_data()

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
    daycpc = {"text": data["daycpc"][0] + " - " + data["daycpc"][-1], "verticalAlign": 'bottom', "align": 'right'}

    ####################
    ##### Neph_UBI #####
    ####################

    chartNeph = {"renderTo": chartIDNeph, "type": chart_type_neph, "height": chart_height, }
    titleNeph = {"text": 'Neph UBI'}
    xAxisNeph = {"title": {"text": 'Time'}, "categories": data['IDneph']}
    yAxisNeph = [{"title": {"text": 'σs/Mm<sup>-1 *10^6'}, },{"title": {"text": 'bs/Mm-1 *10^6'},"opposite": "true"}] #TODO : Opposite axis
    seriesNeph = [
        {"name": 'sBlue',     "yAxis": 0,  "data": data['sblue'],   "color":"#333fff",    "marker": {"symbol": "triangle"}  },
        {"name": 'sRed',      "yAxis": 0,  "data": data['sred'],    "color":"#ff3333",    "marker": {"symbol": "triangle"}    },
        {"name": 'sGreen',    "yAxis": 0,  "data": data['sgreen'],  "color":"#33ff49",    "marker": {"symbol": "triangle"}    },
        {"name": 'bBlue',  "yAxis": 1,  "data": data['bsblue'],  "color":"#b8bcfc",    "marker": {"symbol": "circle"}  },
        {"name": 'bRed',   "yAxis": 1,  "data": data['bsred'],   "color":"#fab9b9",    "marker": {"symbol": "circle"}    },
        {"name": 'bGreen', "yAxis": 1,  "data": data['bsgreen'], "color":"#b5f7bc",    "marker": {"symbol": "circle"}    },
    ]
    dayneph = {"text" : data["dayneph"][0] + " - " + data["dayneph"][-1], "verticalAlign": 'bottom', "align": 'right'}

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
    daypsap = {"text": data["daypsap"][0] + " - " + data["daypsap"][-1], "verticalAlign": 'bottom', "align": 'right'}




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
    xAxisAps= {"title": {"text": 'Time'}, "categories": data['IDaps'],}
    yAxisAps= {
        "title": {"text": 'Particule size'},
        "categories": ['<0.523','0.542','0.583','0.626','0.723','0.777','0.835','0.898','0.965','1.037','1.114','1.197','1.286','1.382','1;486','1.596','1.715','1.843','1.981','2.129','2.288','2.458','2.642','2.839','3.051','3.278','3.523','3.786','4.068','4.371','4.698','5.048','5.425','5.829','6.264','6.732','7.234','7.774','8.354','8.977','9.647','10.37','11.14'], #'type': 'logarithmic', #precise logarithmic scale define upper limit
    }
    dayaps = {"text" : data["dayaps"][0] + " - " + data["dayaps"][-1], "verticalAlign": 'bottom', "align": 'right'}
    datatest1 = data['d1']
    datatest2 = data['d2']
    datatest3 = data['d3']
    datatest4 = data['d4']
    datatest5 = data['d5']
    datatest6 = data['d6']
    datatest7 = data['d7']
    datatest8 = data['d8']
    datatest9 = data['d9']
    datatest10 = data['d10']
    datatest11 = data['d11']
    datatest12 = data['d12']
    datatest13 = data['d13']
    datatest14 = data['d14']
    datatest15 = data['d15']
    datatest16 = data['d16']
    datatest17 = data['d17']
    datatest18 = data['d18']
    datatest19 = data['d19']
    datatest20 = data['d20']
    datatest21 = data['d21']
    datatest22 = data['d22']
    datatest23 = data['d23']
    datatest24 = data['d24']
    datatest25 = data['d25']
    datatest26 = data['d26']
    datatest27 = data['d27']
    datatest28 = data['d28']
    datatest29 = data['d29']
    datatest30 = data['d30']
    datatest31 = data['d31']
    datatest32 = data['d32']
    datatest33 = data['d33']
    datatest34 = data['d34']
    datatest35 = data['d35']
    datatest36 = data['d36']
    datatest37 = data['d37']
    datatest38 = data['d38']
    datatest39 = data['d39']
    datatest40 = data['d40']
    datatest41 = data['d41']
    datatest42 = data['d42']
    datatest43 = data['d43']









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
                                        'dayaps' : dayaps,
        'datatest1': datatest1,
        'datatest2': datatest2,
        'datatest3': datatest3,
        'datatest4': datatest4,
        'datatest5': datatest5,
        'datatest6': datatest6,
        'datatest7': datatest7,
        'datatest8': datatest8,
        'datatest9': datatest9,
        'datatest10': datatest10,
        'datatest11': datatest11,
        'datatest12': datatest12,
        'datatest13': datatest13,
        'datatest14': datatest14,
        'datatest15': datatest15,
        'datatest16': datatest16,
        'datatest17': datatest17,
        'datatest18': datatest18,
        'datatest19': datatest19,
        'datatest20': datatest20,
        'datatest21': datatest21,
        'datatest22': datatest22,
        'datatest23': datatest23,
        'datatest24': datatest24,
        'datatest25': datatest25,
        'datatest26': datatest26,
        'datatest27': datatest27,
        'datatest28': datatest28,
        'datatest29': datatest29,
        'datatest30': datatest30,
        'datatest31': datatest31,
        'datatest32': datatest32,
        'datatest33': datatest33,
        'datatest34': datatest34,
        'datatest35': datatest35,
        'datatest36': datatest36,
        'datatest37': datatest37,
        'datatest38': datatest38,
        'datatest39': datatest39,
        'datatest40': datatest40,
        'datatest41': datatest41,
        'datatest42': datatest42,
        'datatest43': datatest43,

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



def data4(request):
    # resultdisplay = cpc.objects.all()

    cpc3display = psap.objects.using('dataGOA').order_by('-time')[1:10] #all()
    return render(request, "data4.html", {'psap': cpc3display})

