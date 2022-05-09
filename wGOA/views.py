
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

from django.conf import settings
from django.core.mail import send_mail

from .forms import ContactForm, DateForm

# from .calendar_API import test_calendar
################ camera START
from django.http.response import StreamingHttpResponse
from .camera import IPWebCam

from django.http import FileResponse
import os

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

    context = {'segment': 'index'}

    html_template = loader.get_template('index.html')


    return HttpResponse(html_template.render(context, request))

def station(request):
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
            email_subject = f'New contact {form.cleaned_data["email"]}: {form.cleaned_data["subject"]}'
            email_message = form.cleaned_data['message']
            send_mail(email_subject, email_message, settings.CONTACT_EMAIL, settings.ADMIN_EMAIL)
            print(email_subject, email_message, settings.CONTACT_EMAIL, settings.ADMIN_EMAIL)
            return render(request, 'success.html')

    form = ContactForm()
    context = {'form': form, 'segment': 'contact'}

    return render(request, 'contact.html', context)



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

    resultdisplay = neph2.objects.using('dataGOA').order_by('time')[:10] #Just to get the X lasts elements of the list
    cpcdisplay = cpc3.objects.using('dataGOA').order_by('time')[:10]
    psapdisplay = psap.objects.using('dataGOA').order_by('time')[:10]
    apsdisplay = aps.objects.using('dataGOA').order_by('time')[:10]

    return render(request, "data.html", {'neph2': resultdisplay, 'cpc2': cpcdisplay, 'aps' : apsdisplay, 'psap' : psapdisplay})

def data2(request):
    # resultdisplay = cpc2.objects.order_by('ID')[:10] #Just to get the X lasts elements of the list

    dataset = cpc.objects.using('dataGOA').order_by('time')[:10]

    return render(request, 'data2.html', {'dataset': dataset})




########### Graphs     https://stackoverflow.com/questions/27810087/passing-django-database-queryset-to-highcharts-via-json
class ChartData(object):
    def check_the_data():


        data = {'ID': [], 'N': [], 'daycpc': [],
                'IDneph': [], 'sblue': [], 'sred' : [], 'sgreen': [],'bsblue': [], 'bsred' : [], 'bsgreen': [], 'dayneph': [],
                'IDaps': [], 'd1': [],'d2': [], 'd3': [], 'd4': [],'d5': [],'d6': [],'d7': [],'d8': [],'d9': [],'d10': [], 'dayaps': [], 'd11': [],'d12': [], 'd13': [], 'd14': [],'d15': [],'d16': [],'d17': [],'d18': [],'d19': [],'d20': [],'d21': [],'d22': [], 'd23': [], 'd24': [],'d25': [],'d26': [],'d27': [],'d28': [],'d29': [],'d30': [],'d31': [],'d32': [], 'd33': [], 'd34': [],'d35': [],'d36': [],'d37': [],'d38': [],'d39': [],'d40': [],'d41': [],'d42': [],'d43':[],
                'newIDaps': [], 'newdayaps': [],
                'newd1': [], 'newd2': [], 'newd3': [], 'newd4': [], 'newd5': [], 'newd6': [], 'newd7': [], 'newd8': [],
                'newd9': [], 'newd10': [],
                'newd11': [], 'newd12': [], 'newd13': [], 'newd14': [], 'newd15': [], 'newd16': [], 'newd17': [],
                'newd18': [], 'newd19': [], 'newd20': [],
                'newd21': [], 'newd22': [], 'newd23': [], 'newd24': [], 'newd25': [], 'newd26': [], 'newd27': [],
                'newd28': [], 'newd29': [], 'newd30': [],
                'newd31': [], 'newd32': [], 'newd33': [], 'newd34': [], 'newd35': [], 'newd36': [], 'newd37': [],
                'newd38': [], 'newd39': [], 'newd40': [],
                'newd41': [], 'newd42': [], 'newd43': [],

                'IDpsap': [], 'pblue': [], 'pred': [], 'pgreen': [], 'daypsap': [],'newIDpsap': [], 'newblue':[], 'newred': [], 'newgreen': [], 'newdaypsap': [],
                }

        ###################
        ##### CPC_UBI #####
        ###################

        # cpces = cpc2.objects.all() # we take all the items
        # cpces = cpc2.objects.order_by('ID')[:288]  # we take only 40 items

        cpc3display = cpc3.objects.using('dataGOA').order_by('-time')[:288]


        for unit in cpc3display:
            data['ID'].insert(0,datetime.fromtimestamp(unit.time/1000).strftime("%H:%M")) #change the timestamp
            data['daycpc'].insert(0,datetime.fromtimestamp(unit.time/1000).strftime("%Y/%m/%d"))
            data['N'].insert(0,unit.N)






        ####################
        ##### Neph_UBI #####
        ####################
        nephes = neph2.objects.using('dataGOA').order_by('-time')[:1440]

        downLimit = 0

        for unity in nephes:

            data['IDneph'].insert(0,datetime.fromtimestamp(unity.time/1000).strftime( "%H:%M"))
            data['dayneph'].insert(0,datetime.fromtimestamp(unity.time/ 1000).strftime("%Y/%m/%d"))
            data['sblue'].insert(0, isSmallerThan(unity.sblue * 1000000, downLimit)) # x 10^6
            data['sred'].insert(0,isSmallerThan(unity.sred * 1000000, downLimit))
            data['sgreen'].insert(0,isSmallerThan(unity.sgreen * 1000000, downLimit))
            data['bsblue'].insert(0,isSmallerThan(unity.bsblue * 1000000, downLimit))
            data['bsred'].insert(0,isSmallerThan(unity.bsred * 1000000, downLimit))
            data['bsgreen'].insert(0,isSmallerThan(unity.bsgreen * 1000000, downLimit))


        ####################
        ##### PSAP_UBI #####
        ####################
        psapes = psap.objects.using('dataGOA').order_by('-time')[1:1440]

        for unites in psapes:
            data['IDpsap'].insert(0,datetime.fromtimestamp(unites.time/1000).strftime( "%H:%M"))            # https://www.codegrepper.com/code-examples/python/get+every+nth+element+in+list+python
            data['daypsap'].insert(0,datetime.fromtimestamp(unites.time/ 1000).strftime("%Y/%m/%d"))
            data['pblue'].insert(0,isSmallerThan(unites.blue, downLimit))
            data['pred'].insert(0,isSmallerThan(unites.red, downLimit))
            data['pgreen'].insert(0,isSmallerThan(unites.green, downLimit))

################################################################

        # downsampling :
        # x = 0
        # while x < 75555:
        #
        #     newpsapdisplay = psap.objects.using('dataGOA').order_by('-time')[x:x + 100]
        #
        #     for unit in newpsapdisplay:
        #         data['pblue'].insert(0, unit.blue)
        #         data['pred'].insert(0, unit.red)
        #         data['pgreen'].insert(0, unit.green)
        #
        #         data['IDpsap'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%H:%M"))
        #         data['daypsap'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%Y/%m/%d"))
        #
        #     # print(data['blue'], data['red'], data['green'])
        #
        #     avgBlue = sum(data['pblue']) / len(data['pblue'])
        #     avgRed = sum(data['pred']) / len(data['pred'])
        #     avgGreen = sum(data['pgreen']) / len(data['pgreen'])
        #
        #     data['newblue'].insert(0, avgBlue)
        #     data['newred'].insert(0, avgRed)
        #     data['newgreen'].insert(0, avgGreen)
        #
        #     data['newIDpsap'].insert(0, data['IDpsap'][0])
        #     data['newdaypsap'].insert(0, data['daypsap'][0])
        #
        #     # print('blue',avgBlue, 'red', avgRed, 'green', avgGreen)
        #
        #     x = x + 100
        #



        ###################
        ##### APS_UBI #####
        ###################
        apses = aps.objects.using('dataGOA').order_by('-time')[:144]        #.filter(time__endswith='65000')
        # print(apses)
        # print(apses)

        # time_to_exclude = ['265000', '865000', '765000', '565000',  '465000']
        # apsess = aps.objects.using('dataGOA').order_by('-time')
        # for exclude_time in time_to_exclude:
        #     apsess = apsess.exclude(time__endswith=exclude_time)
        # erg = apsess[:144]
        #
        # print("apsess", erg)

######################## WORKING ####################################
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


################################# TEST #######################

        # y = 0
        # while y < 235:
        #
        #     apses = aps.objects.using('dataGOA').order_by('-time')[y:y + 5]
        #     # print(apses)
        #
        #     upperLimit = 600
        #
        #     for unita in apses:
        #         data['IDaps'].insert(0, datetime.fromtimestamp(unita.time / 1000).strftime("%H:%M"))
        #         data['dayaps'].insert(0, datetime.fromtimestamp(unita.time / 1000).strftime("%Y/%m/%d"))
        #         data['d1'].insert(0, unita.d1)
        #         data['d2'].insert(0, unita.d2)
        #         data['d3'].insert(0, unita.d3)
        #         data['d4'].insert(0, unita.d4)
        #         data['d5'].insert(0, unita.d5)
        #         data['d6'].insert(0, unita.d6)
        #         data['d7'].insert(0, unita.d7)
        #         data['d8'].insert(0, unita.d8)
        #         data['d9'].insert(0, unita.d9)
        #         data['d10'].insert(0, unita.d10)
        #         data['d11'].insert(0, unita.d11)
        #         data['d12'].insert(0, unita.d12)
        #         data['d13'].insert(0, unita.d13)
        #         data['d14'].insert(0, unita.d14)
        #         data['d15'].insert(0, unita.d15)
        #         data['d16'].insert(0, unita.d16)
        #         data['d17'].insert(0, unita.d17)
        #         data['d18'].insert(0, unita.d18)
        #         data['d19'].insert(0, unita.d19)
        #         data['d20'].insert(0, unita.d20)
        #         data['d21'].insert(0, unita.d21)
        #         data['d22'].insert(0, unita.d22)
        #         data['d23'].insert(0, unita.d23)
        #         data['d24'].insert(0, unita.d24)
        #         data['d25'].insert(0, unita.d25)
        #         data['d26'].insert(0, unita.d26)
        #         data['d27'].insert(0, unita.d27)
        #         data['d28'].insert(0, unita.d28)
        #         data['d29'].insert(0, unita.d29)
        #         data['d30'].insert(0, unita.d30)
        #         data['d31'].insert(0, unita.d31)
        #         data['d32'].insert(0, unita.d32)
        #         data['d33'].insert(0, unita.d33)
        #         data['d34'].insert(0, unita.d34)
        #         data['d35'].insert(0, unita.d35)
        #         data['d36'].insert(0, unita.d36)
        #         data['d37'].insert(0, unita.d37)
        #         data['d38'].insert(0, unita.d38)
        #         data['d39'].insert(0, unita.d39)
        #         data['d40'].insert(0, unita.d40)
        #         data['d41'].insert(0, unita.d41)
        #         data['d42'].insert(0, unita.d42)
        #         data['d43'].insert(0, unita.d43)
        #
        #     avgd1 = sum(data['d1']) / len(data['d1'])
        #     avgd2 = sum(data['d2']) / len(data['d2'])
        #     avgd3 = sum(data['d3']) / len(data['d3'])
        #     avgd4 = sum(data['d4']) / len(data['d4'])
        #     avgd5 = sum(data['d5']) / len(data['d5'])
        #     avgd6 = sum(data['d6']) / len(data['d6'])
        #     avgd7 = sum(data['d7']) / len(data['d7'])
        #     avgd8 = sum(data['d8']) / len(data['d8'])
        #     avgd9 = sum(data['d9']) / len(data['d9'])
        #     avgd10 = sum(data['d10']) / len(data['d10'])
        #     avgd11 = sum(data['d11']) / len(data['d11'])
        #     avgd12 = sum(data['d12']) / len(data['d12'])
        #     avgd13 = sum(data['d13']) / len(data['d13'])
        #     avgd14 = sum(data['d14']) / len(data['d14'])
        #     avgd15 = sum(data['d15']) / len(data['d15'])
        #     avgd16 = sum(data['d16']) / len(data['d16'])
        #     avgd17 = sum(data['d17']) / len(data['d17'])
        #     avgd18 = sum(data['d18']) / len(data['d18'])
        #     avgd19 = sum(data['d19']) / len(data['d19'])
        #     avgd20 = sum(data['d20']) / len(data['d20'])
        #     avgd21 = sum(data['d21']) / len(data['d21'])
        #     avgd22 = sum(data['d22']) / len(data['d22'])
        #     avgd23 = sum(data['d23']) / len(data['d23'])
        #     avgd24 = sum(data['d24']) / len(data['d24'])
        #     avgd25 = sum(data['d25']) / len(data['d25'])
        #     avgd26 = sum(data['d26']) / len(data['d26'])
        #     avgd27 = sum(data['d27']) / len(data['d27'])
        #     avgd28 = sum(data['d28']) / len(data['d28'])
        #     avgd29 = sum(data['d29']) / len(data['d29'])
        #     avgd30 = sum(data['d30']) / len(data['d30'])
        #     avgd31 = sum(data['d31']) / len(data['d31'])
        #     avgd32 = sum(data['d32']) / len(data['d32'])
        #     avgd33 = sum(data['d33']) / len(data['d33'])
        #     avgd34 = sum(data['d34']) / len(data['d34'])
        #     avgd35 = sum(data['d35']) / len(data['d35'])
        #     avgd36 = sum(data['d36']) / len(data['d36'])
        #     avgd37 = sum(data['d37']) / len(data['d37'])
        #     avgd38 = sum(data['d38']) / len(data['d38'])
        #     avgd39 = sum(data['d39']) / len(data['d39'])
        #     avgd40 = sum(data['d40']) / len(data['d40'])
        #     avgd41 = sum(data['d41']) / len(data['d41'])
        #     avgd42 = sum(data['d42']) / len(data['d42'])
        #     avgd43 = sum(data['d43']) / len(data['d43'])
        #
        #     data['newd1'].insert(0, isGreaterThan(avgd1, upperLimit))
        #     data['newd2'].insert(0, isGreaterThan(avgd2, upperLimit))
        #     data['newd3'].insert(0, isGreaterThan(avgd3, upperLimit))
        #     data['newd4'].insert(0, isGreaterThan(avgd4, upperLimit))
        #     data['newd5'].insert(0, isGreaterThan(avgd5, upperLimit))
        #     data['newd6'].insert(0, isGreaterThan(avgd6, upperLimit))
        #     data['newd7'].insert(0, isGreaterThan(avgd7, upperLimit))
        #     data['newd8'].insert(0, isGreaterThan(avgd8, upperLimit))
        #     data['newd9'].insert(0, isGreaterThan(avgd9, upperLimit))
        #     data['newd10'].insert(0, isGreaterThan(avgd10, upperLimit))
        #     data['newd11'].insert(0, isGreaterThan(avgd11, upperLimit))
        #     data['newd12'].insert(0, isGreaterThan(avgd12, upperLimit))
        #     data['newd13'].insert(0, isGreaterThan(avgd13, upperLimit))
        #     data['newd14'].insert(0, isGreaterThan(avgd14, upperLimit))
        #     data['newd15'].insert(0, isGreaterThan(avgd15, upperLimit))
        #     data['newd16'].insert(0, isGreaterThan(avgd16, upperLimit))
        #     data['newd17'].insert(0, isGreaterThan(avgd17, upperLimit))
        #     data['newd18'].insert(0, isGreaterThan(avgd18, upperLimit))
        #     data['newd19'].insert(0, isGreaterThan(avgd19, upperLimit))
        #     data['newd20'].insert(0, isGreaterThan(avgd20, upperLimit))
        #     data['newd21'].insert(0, isGreaterThan(avgd21, upperLimit))
        #     data['newd22'].insert(0, isGreaterThan(avgd22, upperLimit))
        #     data['newd23'].insert(0, isGreaterThan(avgd23, upperLimit))
        #     data['newd24'].insert(0, isGreaterThan(avgd24, upperLimit))
        #     data['newd25'].insert(0, isGreaterThan(avgd25, upperLimit))
        #     data['newd26'].insert(0, isGreaterThan(avgd26, upperLimit))
        #     data['newd27'].insert(0, isGreaterThan(avgd27, upperLimit))
        #     data['newd28'].insert(0, isGreaterThan(avgd28, upperLimit))
        #     data['newd29'].insert(0, isGreaterThan(avgd29, upperLimit))
        #     data['newd30'].insert(0, isGreaterThan(avgd30, upperLimit))
        #     data['newd31'].insert(0, isGreaterThan(avgd31, upperLimit))
        #     data['newd32'].insert(0, isGreaterThan(avgd32, upperLimit))
        #     data['newd33'].insert(0, isGreaterThan(avgd33, upperLimit))
        #     data['newd34'].insert(0, isGreaterThan(avgd34, upperLimit))
        #     data['newd35'].insert(0, isGreaterThan(avgd35, upperLimit))
        #     data['newd36'].insert(0, isGreaterThan(avgd36, upperLimit))
        #     data['newd37'].insert(0, isGreaterThan(avgd37, upperLimit))
        #     data['newd38'].insert(0, isGreaterThan(avgd38, upperLimit))
        #     data['newd39'].insert(0, isGreaterThan(avgd39, upperLimit))
        #     data['newd40'].insert(0, isGreaterThan(avgd40, upperLimit))
        #     data['newd41'].insert(0, isGreaterThan(avgd41, upperLimit))
        #     data['newd42'].insert(0, isGreaterThan(avgd42, upperLimit))
        #     data['newd43'].insert(0, isGreaterThan(avgd43, upperLimit))
        #
        #     # print(data['newd1'])
        #
        #     data['newIDaps'].insert(0, data['IDaps'][0])
        #     data['newdayaps'].insert(0, data['dayaps'][0])
        #
        #     # print('blue',avgBlue, 'red', avgRed, 'green', avgGreen)
        #
        #     y = y + 5
        #
        ###########################################################
        return data

def isGreaterThan(x,y):
    if x>y:
        x = y
    else :
        x = x

    return x

def isSmallerThan(x,y):
    if x<y:
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





# import numpy as np
# import pandas as pd


def test(request):
    context = {}  # used to pass the info to the HTML
    # resultdisplay = cpc.objects.all()
    #
    # cpc3display = cpc2.objects.order_by('-ID')[1:10] #all()
    #
    #
    # context['psap'] = cpc3display
    #
    #
    # # downSampling()
    # APSdownSampling()
    t = time.time()
    downSampling3()
    elapsed = time.time() - t
    print('time = ', elapsed)
    # data = {'IDpsap': [], 'daypsap': [], 'blue': [], 'red': [], 'green': [], 'newblue': [], 'newred': [], 'newgreen': [],'newIDpsap': [], 'newdaypsap': [],}
    #
    # psapdisplay_det = psap.objects.using('dataGOA').order_by('-time')[:100000]
    #
    # for unit in psapdisplay_det:
    #     data['blue'].insert(0, unit.blue)
    #     data['red'].insert(0, unit.red)
    #     data['green'].insert(0, unit.green)
    #     data['daypsap'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%Y/%m/%d - %H:%M:%S"))
    #
    #
    #
    #
    # context['blue'] = data['blue']
    # context['red'] = data['red']
    # context['green'] = data['green']
    # context['daypsap'] = data['daypsap']

    return render(request, "test.html", context)




def Dcpc_det(request):
    context = {}  # used to pass the info to the HTML
    yoda = {'daysList': []}

    theDaysData = cpc3.objects.using('dataGOA').order_by('-time').all()
    day1 = 0
    month1 = 0
    for days in theDaysData:
        day2 = datetime.fromtimestamp(days.time / 1000).strftime("%Y/%m/%d")
        month2 = datetime.fromtimestamp(days.time / 1000).strftime("%Y/%m")
        if day2 != day1:
            yoda['daysList'].insert(0, datetime.fromtimestamp(days.time / 1000).strftime("%Y/%m/%d"))
        # if month2 != month1:
        #     yoda['daysList'].insert(0, '<br>')
        day1 = day2
        month1 = month2
    # print(yoda['daysList'])
    context['daysList'] = yoda['daysList']

    return render(request, 'data_det/cpcD.html',  context)

def Daps_det(request):
    context = {}  # used to pass the info to the HTML
    yoda = {'daysList': []}

    theDaysData = aps.objects.using('dataGOA').order_by('-time').all()
    day1 = 0
    month1 = 0
    for days in theDaysData:
        day2 = datetime.fromtimestamp(days.time / 1000).strftime("%Y/%m/%d")
        month2 = datetime.fromtimestamp(days.time / 1000).strftime("%Y/%m")
        if day2 != day1:
            yoda['daysList'].insert(0, datetime.fromtimestamp(days.time / 1000).strftime("%Y/%m/%d"))
        # if month2 != month1:
        #     yoda['daysList'].insert(0, '<br>')
        day1 = day2
        month1 = month2
    # print(yoda['daysList'])
    context['daysList'] = yoda['daysList']

    return render(request, 'data_det/apsD.html',  context)

def Dneph_det(request):
    context = {}  # used to pass the info to the HTML
    yoda = {'daysList': []}

    theDaysData = neph2.objects.using('dataGOA').order_by('-time').all()
    day1 = 0
    month1 = 0
    for days in theDaysData:
        day2 = datetime.fromtimestamp(days.time / 1000).strftime("%Y/%m/%d")
        month2 = datetime.fromtimestamp(days.time / 1000).strftime("%Y/%m")
        if day2 != day1:
            yoda['daysList'].insert(0, datetime.fromtimestamp(days.time / 1000).strftime("%Y/%m/%d"))
        # if month2 != month1:
        #     yoda['daysList'].insert(0, '<br>')
        day1 = day2
        month1 = month2
    # print(yoda['daysList'])
    context['daysList'] = yoda['daysList']

    return render(request, 'data_det/nephD.html',  context)


def Dpsap_det(request):
    context = {}  # used to pass the info to the HTML
    yoda = {'daysList': []}

    theDaysData = psap.objects.using('dataGOA').order_by('-time').all()
    day1 = 0
    month1 = 0
    for days in theDaysData:
        day2 = datetime.fromtimestamp(days.time / 1000).strftime("%Y/%m/%d")
        month2 = datetime.fromtimestamp(days.time / 1000).strftime("%Y/%m")
        if day2 != day1:
            yoda['daysList'].insert(0, datetime.fromtimestamp(days.time / 1000).strftime("%Y/%m/%d"))
        # if month2 != month1:
        #     yoda['daysList'].insert(0, '<br>')
        day1 = day2
        month1 = month2
    # print(yoda['daysList'])
    context['daysList'] = yoda['daysList']

    return render(request, 'data_det/psapD.html',  context)


def cpc_det(request):
    # data = cpcDetData.cpc_det_data()
    # print("data is ", data)
    context = {} #used to pass the info to the HTML
    form = DateForm() #used to get the form data
    context['form'] = form #adding the form to the list of variable passed to the html
    # data = {'ID': [], 'N': [], 'daycpc': []} #creating the structure for the data
    yoda = {'ID': [], 'N': [], 'daycpc': [], 'daysList':[]}



    if request.GET: # getting data from the form

        # TODO: transform start and end to unix to choose the correct data

        #########################################
        start_year = int(request.GET['start_year'])
        start_month = int(request.GET['start_month'])
        start_day = int(request.GET['start_day'])
        try:
            dt = datetime(year=start_year, month=start_month, day=start_day)
        except ValueError:
            return render(request, 'data_det/cpc.html',  context)
        value = int(time.mktime(dt.timetuple()))




        # QUERIES :
        # https: // docs.djangoproject.com / en / 4.0 / topics / db / queries /

        value = int(value/10000)
        # print("value is : ",value)
        precisedata = cpc3.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value) # returns a QuerySet : <class 'django.db.models.query.QuerySet'>

        value = value+1
        precisedata2 = cpc3.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value)

        value = value + 1
        precisedata3 = cpc3.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value)

        value = value + 1
        precisedata4 = cpc3.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value)

        value = value + 1
        precisedata5 = cpc3.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value)

        value = value + 1
        precisedata6 = cpc3.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value)

        value = value + 1
        precisedata7 = cpc3.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value)

        value = value + 1
        precisedata8 = cpc3.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value)

        value = value + 1
        precisedata9 = cpc3.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value)

        for unit in precisedata9:
            yoda['ID'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%H:%M"))  # change the timestamp
            yoda['daycpc'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%Y/%m/%d"))
            yoda['N'].insert(0, unit.N)

        for unit in precisedata8:
            yoda['ID'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%H:%M"))  # change the timestamp
            yoda['daycpc'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%Y/%m/%d"))
            yoda['N'].insert(0, unit.N)

        for unit in precisedata7:
            yoda['ID'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%H:%M"))  # change the timestamp
            yoda['daycpc'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%Y/%m/%d"))
            yoda['N'].insert(0, unit.N)

        for unit in precisedata6:
            yoda['ID'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%H:%M"))  # change the timestamp
            yoda['daycpc'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%Y/%m/%d"))
            yoda['N'].insert(0, unit.N)

        for unit in precisedata5:
            yoda['ID'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%H:%M"))  # change the timestamp
            yoda['daycpc'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%Y/%m/%d"))
            yoda['N'].insert(0, unit.N)

        for unit in precisedata4:
            yoda['ID'].insert(0,datetime.fromtimestamp(unit.time/1000).strftime("%H:%M")) #change the timestamp
            yoda['daycpc'].insert(0,datetime.fromtimestamp(unit.time/1000).strftime("%Y/%m/%d"))
            yoda['N'].insert(0,unit.N)

        for unit in precisedata3:
            yoda['ID'].insert(0,datetime.fromtimestamp(unit.time/1000).strftime("%H:%M")) #change the timestamp
            yoda['daycpc'].insert(0,datetime.fromtimestamp(unit.time/1000).strftime("%Y/%m/%d"))
            yoda['N'].insert(0,unit.N)

        for unit in precisedata2:
            yoda['ID'].insert(0,datetime.fromtimestamp(unit.time/1000).strftime("%H:%M")) #change the timestamp
            yoda['daycpc'].insert(0,datetime.fromtimestamp(unit.time/1000).strftime("%Y/%m/%d"))
            yoda['N'].insert(0,unit.N)


        for unit in precisedata:
            yoda['ID'].insert(0,datetime.fromtimestamp(unit.time/1000).strftime("%H:%M")) #change the timestamp
            yoda['daycpc'].insert(0,datetime.fromtimestamp(unit.time/1000).strftime("%Y/%m/%d"))
            yoda['N'].insert(0,unit.N)

        # print("time : ",yoda['ID'])
        ##############################################

        # WORKING :

        # start = int(request.GET['start'])  # start date
        # end = int(request.GET['end'])  # end date

        # cpc3display_det = cpc3.objects.using('dataGOA').order_by('-time')[end-1:end]

        # print(type(cpc3display_det))

        # for unit in cpc3display_det:    # saving data in the correct format
        #     data['ID'].insert(0,datetime.fromtimestamp(unit.time/1000).strftime("%H:%M")) #change the timestamp
        #     data['daycpc'].insert(0,datetime.fromtimestamp(unit.time/1000).strftime("%Y/%m/%d"))
        #     data['N'].insert(0,unit.N)
        # print(type(data))
    ############ GRAPH ############
        cpcdet = "cpcdet"

        chart = {"renderTo": cpcdet, "type": "line", "height": 500, }
        title = {"text": 'CPC UBI'}
        xAxis = {"title": {"text": 'Time'}, "categories": yoda['ID']}
        yAxis = {"title": {"text": 'N/#/cm3'}}
        series = [
            {"name": 'N/#/cm3', "data": yoda['N'], "color": "#333fff"},
        ]
        try:
            Ddaycpc = {"text": yoda["daycpc"][0] + " - " + yoda["daycpc"][-1], "verticalAlign": 'bottom', "align": 'right'}
        except IndexError:
            Ddaycpc = {"text": "Try again, no value", "verticalAlign": 'bottom', "align": 'right'}
            title = {"text": 'NO VALUES'}

        # add the data to the context to send it to the html



        context['cpcdet']= cpcdet
        context['chart']= chart
        context['series']= series
        context['title']= title
        context['xAxis']= xAxis
        context['yAxis']= yAxis
        context['Ddaycpc']= Ddaycpc

        # context['cpc3display_det'] = cpc3display_det
        context['N']        = yoda['N']     #data['N']
        context['ID']       = yoda['ID']        #data['ID']
        context['daycpc']   = yoda['daycpc']        #data['daycpc']

        # context['start'] = start
        # context['end'] = end
        try:
            context['titleday'] = yoda["daycpc"][0] + " - " + yoda["daycpc"][-1]
        except IndexError:
            context['titleday'] = datetime(year=start_year, month=start_month, day=start_day)

        context['dateTimeDD'] = datetime(year=start_year, month=start_month, day=start_day)

        # context['precisedata'] = precisedata


        # print(type(context['cpc3display_det']))


    return render(request, 'data_det/cpc.html',  context)





def neph_det(request):
    # data = cpcDetData.cpc_det_data()
    # print("data is ", data)
    context = {}
    form = DateForm()
    context['form'] = form
    data = { 'IDneph': [], 'sblue': [], 'sred' : [], 'sgreen': [],'bsblue': [], 'bsred' : [], 'bsgreen': [], 'dayneph': [],}



    if request.GET:

        # WORKING :

        start_year = int(request.GET['start_year'])
        start_month = int(request.GET['start_month'])
        start_day = int(request.GET['start_day'])
        try:
            dt = datetime(year=start_year, month=start_month, day=start_day)
        except ValueError:
            return render(request, 'data_det/neph.html', context)
        value = int(time.mktime(dt.timetuple()))

        value = int(value / 10000)
        nephdisplay_det = neph2.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value)

        value = value+1
        nephdisplay_det2 = neph2.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value)

        value = value + 1
        nephdisplay_det3 = neph2.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value)

        value = value + 1
        nephdisplay_det4 = neph2.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value)

        value = value + 1
        nephdisplay_det5 = neph2.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value)

        value = value + 1
        nephdisplay_det6 = neph2.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value)

        value = value + 1
        nephdisplay_det7 = neph2.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value)

        value = value + 1
        nephdisplay_det8 = neph2.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value)

        value = value + 1
        nephdisplay_det9 = neph2.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value)

        value = value + 1
        nephdisplay_det10 = neph2.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value)

        for unity in nephdisplay_det10:
            data['IDneph'].insert(0, datetime.fromtimestamp(unity.time / 1000).strftime("%H:%M"))
            data['dayneph'].insert(0, datetime.fromtimestamp(unity.time / 1000).strftime("%Y/%m/%d"))
            data['sblue'].insert(0, unity.sblue * 1000000)  # x 10^6
            data['sred'].insert(0, unity.sred * 1000000)
            data['sgreen'].insert(0, unity.sgreen * 1000000)
            data['bsblue'].insert(0, unity.bsblue * 1000000)
            data['bsred'].insert(0, unity.bsred * 1000000)
            data['bsgreen'].insert(0, unity.bsgreen * 1000000)

        for unity in nephdisplay_det9:
            data['IDneph'].insert(0, datetime.fromtimestamp(unity.time / 1000).strftime("%H:%M"))
            data['dayneph'].insert(0, datetime.fromtimestamp(unity.time / 1000).strftime("%Y/%m/%d"))
            data['sblue'].insert(0, unity.sblue * 1000000)  # x 10^6
            data['sred'].insert(0, unity.sred * 1000000)
            data['sgreen'].insert(0, unity.sgreen * 1000000)
            data['bsblue'].insert(0, unity.bsblue * 1000000)
            data['bsred'].insert(0, unity.bsred * 1000000)
            data['bsgreen'].insert(0, unity.bsgreen * 1000000)

        for unity in nephdisplay_det8:
            data['IDneph'].insert(0, datetime.fromtimestamp(unity.time / 1000).strftime("%H:%M"))
            data['dayneph'].insert(0, datetime.fromtimestamp(unity.time / 1000).strftime("%Y/%m/%d"))
            data['sblue'].insert(0, unity.sblue * 1000000)  # x 10^6
            data['sred'].insert(0, unity.sred * 1000000)
            data['sgreen'].insert(0, unity.sgreen * 1000000)
            data['bsblue'].insert(0, unity.bsblue * 1000000)
            data['bsred'].insert(0, unity.bsred * 1000000)
            data['bsgreen'].insert(0, unity.bsgreen * 1000000)

        for unity in nephdisplay_det7:
            data['IDneph'].insert(0, datetime.fromtimestamp(unity.time / 1000).strftime("%H:%M"))
            data['dayneph'].insert(0, datetime.fromtimestamp(unity.time / 1000).strftime("%Y/%m/%d"))
            data['sblue'].insert(0, unity.sblue * 1000000)  # x 10^6
            data['sred'].insert(0, unity.sred * 1000000)
            data['sgreen'].insert(0, unity.sgreen * 1000000)
            data['bsblue'].insert(0, unity.bsblue * 1000000)
            data['bsred'].insert(0, unity.bsred * 1000000)
            data['bsgreen'].insert(0, unity.bsgreen * 1000000)

        for unity in nephdisplay_det6:
            data['IDneph'].insert(0, datetime.fromtimestamp(unity.time / 1000).strftime("%H:%M"))
            data['dayneph'].insert(0, datetime.fromtimestamp(unity.time / 1000).strftime("%Y/%m/%d"))
            data['sblue'].insert(0, unity.sblue * 1000000)  # x 10^6
            data['sred'].insert(0, unity.sred * 1000000)
            data['sgreen'].insert(0, unity.sgreen * 1000000)
            data['bsblue'].insert(0, unity.bsblue * 1000000)
            data['bsred'].insert(0, unity.bsred * 1000000)
            data['bsgreen'].insert(0, unity.bsgreen * 1000000)

        for unity in nephdisplay_det5:
            data['IDneph'].insert(0, datetime.fromtimestamp(unity.time / 1000).strftime("%H:%M"))
            data['dayneph'].insert(0, datetime.fromtimestamp(unity.time / 1000).strftime("%Y/%m/%d"))
            data['sblue'].insert(0, unity.sblue * 1000000)  # x 10^6
            data['sred'].insert(0, unity.sred * 1000000)
            data['sgreen'].insert(0, unity.sgreen * 1000000)
            data['bsblue'].insert(0, unity.bsblue * 1000000)
            data['bsred'].insert(0, unity.bsred * 1000000)
            data['bsgreen'].insert(0, unity.bsgreen * 1000000)

        for unity in nephdisplay_det4:
            data['IDneph'].insert(0, datetime.fromtimestamp(unity.time / 1000).strftime("%H:%M"))
            data['dayneph'].insert(0, datetime.fromtimestamp(unity.time / 1000).strftime("%Y/%m/%d"))
            data['sblue'].insert(0, unity.sblue * 1000000)  # x 10^6
            data['sred'].insert(0, unity.sred * 1000000)
            data['sgreen'].insert(0, unity.sgreen * 1000000)
            data['bsblue'].insert(0, unity.bsblue * 1000000)
            data['bsred'].insert(0, unity.bsred * 1000000)
            data['bsgreen'].insert(0, unity.bsgreen * 1000000)

        for unity in nephdisplay_det3:
            data['IDneph'].insert(0, datetime.fromtimestamp(unity.time / 1000).strftime("%H:%M"))
            data['dayneph'].insert(0, datetime.fromtimestamp(unity.time / 1000).strftime("%Y/%m/%d"))
            data['sblue'].insert(0, unity.sblue * 1000000)  # x 10^6
            data['sred'].insert(0, unity.sred * 1000000)
            data['sgreen'].insert(0, unity.sgreen * 1000000)
            data['bsblue'].insert(0, unity.bsblue * 1000000)
            data['bsred'].insert(0, unity.bsred * 1000000)
            data['bsgreen'].insert(0, unity.bsgreen * 1000000)

        for unity in nephdisplay_det2:
            data['IDneph'].insert(0, datetime.fromtimestamp(unity.time / 1000).strftime("%H:%M"))
            data['dayneph'].insert(0, datetime.fromtimestamp(unity.time / 1000).strftime("%Y/%m/%d"))
            data['sblue'].insert(0, unity.sblue * 1000000)  # x 10^6
            data['sred'].insert(0, unity.sred * 1000000)
            data['sgreen'].insert(0, unity.sgreen * 1000000)
            data['bsblue'].insert(0, unity.bsblue * 1000000)
            data['bsred'].insert(0, unity.bsred * 1000000)
            data['bsgreen'].insert(0, unity.bsgreen * 1000000)

        for unity in nephdisplay_det:
            data['IDneph'].insert(0, datetime.fromtimestamp(unity.time / 1000).strftime("%H:%M"))
            data['dayneph'].insert(0, datetime.fromtimestamp(unity.time / 1000).strftime("%Y/%m/%d"))
            data['sblue'].insert(0, unity.sblue * 1000000)  # x 10^6
            data['sred'].insert(0, unity.sred * 1000000)
            data['sgreen'].insert(0, unity.sgreen * 1000000)
            data['bsblue'].insert(0, unity.bsblue * 1000000)
            data['bsred'].insert(0, unity.bsred * 1000000)
            data['bsgreen'].insert(0, unity.bsgreen * 1000000)

    ############ GRAPH ############
        nephdet = "nephdet"

        chartNeph = {"renderTo": nephdet, "type": "line", "height": 500, }
        titleNeph = {"text": 'Neph UBI'}
        xAxisNeph = {"title": {"text": 'Time'}, "categories": data['IDneph']}
        yAxisNeph = [{"title": {"text": 'σs/Mm<sup>-1 *10^6'}, },
                     {"title": {"text": 'bs/Mm-1 *10^6'}, "opposite": "true"}]  # TODO : Opposite axis
        seriesNeph = [
            {"name": 'sBlue', "yAxis": 0, "data": data['sblue'], "color": "#333fff", "marker": {"symbol": "triangle"}},
            {"name": 'sRed', "yAxis": 0, "data": data['sred'], "color": "#ff3333", "marker": {"symbol": "triangle"}},
            {"name": 'sGreen', "yAxis": 0, "data": data['sgreen'], "color": "#33ff49", "marker": {"symbol": "triangle"}},
            {"name": 'bBlue', "yAxis": 1, "data": data['bsblue'], "color": "#b8bcfc", "marker": {"symbol": "circle"}},
            {"name": 'bRed', "yAxis": 1, "data": data['bsred'], "color": "#fab9b9", "marker": {"symbol": "circle"}},
            {"name": 'bGreen', "yAxis": 1, "data": data['bsgreen'], "color": "#b5f7bc", "marker": {"symbol": "circle"}},
        ]
        try:
            Ddayneph = {"text": data["dayneph"][0] + " - " + data["dayneph"][-1], "verticalAlign": 'bottom',
                   "align": 'right'}
        except IndexError:
            Ddayneph = {"text": "Try again, no value", "verticalAlign": 'bottom', "align": 'right'}
            titleNeph = {"text": 'NO VALUES'}

        # add the data to the context to send it to the html

        context['nephdet']= nephdet
        context['chart']=   chartNeph
        context['seriesNeph']=  seriesNeph
        context['title']=   titleNeph
        context['xAxis']=   xAxisNeph
        context['yAxis']=   yAxisNeph
        context['Ddayneph']= Ddayneph

        try:
            context['titleday'] = data["dayneph"][0] + " - " + data["dayneph"][-1]
        except IndexError:
            context['titleday'] = datetime(year=start_year, month=start_month, day=start_day)

        context['dateTimeDD'] = datetime(year=start_year, month=start_month, day=start_day)


        context['nephdisplay_det'] = nephdisplay_det
        # context['N'] = data['N']
        # context['ID'] = data['ID']
        context['dayneph'] = data['dayneph']



        context['IDneph']=data['IDneph']
        context['dayneph']=data['dayneph']
        context['sblue']=data['sblue']
        context['sred']=data['sred']
        context['sgreen']=data['sgreen']
        context['bsblue']=data['bsblue']
        context['bsred']=data['bsred']
        context['bsgreen']=data['bsgreen']

    return render(request, 'data_det/neph.html',  context)



def aps_det(request):
    context = {}
    form = DateForm()
    context['form'] = form
    data = {'IDaps': [],  'd1': [],'d2': [], 'd3': [], 'd4': [],'d5': [],'d6': [],'d7': [],'d8': [],'d9': [],'d10': [], 'dayaps': [], 'd11': [],'d12': [], 'd13': [], 'd14': [],'d15': [],'d16': [],'d17': [],'d18': [],'d19': [],'d20': [],'d21': [],'d22': [], 'd23': [], 'd24': [],'d25': [],'d26': [],'d27': [],'d28': [],'d29': [],'d30': [],'d31': [],'d32': [], 'd33': [], 'd34': [],'d35': [],'d36': [],'d37': [],'d38': [],'d39': [],'d40': [],'d41': [],'d42': [],'d43':[],}

    if request.GET:

        # WORKING :

        start_year = int(request.GET['start_year'])
        start_month = int(request.GET['start_month'])
        start_day = int(request.GET['start_day'])
        try:
            dt = datetime(year=start_year, month=start_month, day=start_day)
        except ValueError:
            return render(request, 'data_det/aps.html',  context)
        value = int(time.mktime(dt.timetuple()))

        # QUERIES :
        # https: // docs.djangoproject.com / en / 4.0 / topics / db / queries /

        value = int(value/10000)


        apsdisplay_det = aps.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value) # returns a QuerySet : <class 'django.db.models.query.QuerySet'>

        # print(apsdisplay_det)

        upperLimit = 600

        for unita in apsdisplay_det:
            data['IDaps'].insert(0, datetime.fromtimestamp(unita.time / 1000).strftime("%H:%M"))
            data['dayaps'].insert(0, datetime.fromtimestamp(unita.time / 1000).strftime("%Y/%m/%d"))
            data['d1'].insert(0, isGreaterThan(unita.d1, upperLimit))
            data['d2'].insert(0, isGreaterThan(unita.d2, upperLimit))
            data['d3'].insert(0, isGreaterThan(unita.d3, upperLimit))
            data['d4'].insert(0, isGreaterThan(unita.d4, upperLimit))
            data['d5'].insert(0, isGreaterThan(unita.d5, upperLimit))
            data['d6'].insert(0, isGreaterThan(unita.d6, upperLimit))
            data['d7'].insert(0, isGreaterThan(unita.d7, upperLimit))
            data['d8'].insert(0, isGreaterThan(unita.d8, upperLimit))
            data['d9'].insert(0, isGreaterThan(unita.d9, upperLimit))
            data['d10'].insert(0, isGreaterThan(unita.d10, upperLimit))
            data['d11'].insert(0, isGreaterThan(unita.d11, upperLimit))
            data['d12'].insert(0, isGreaterThan(unita.d12, upperLimit))
            data['d13'].insert(0, isGreaterThan(unita.d13, upperLimit))
            data['d14'].insert(0, isGreaterThan(unita.d14, upperLimit))
            data['d15'].insert(0, isGreaterThan(unita.d15, upperLimit))
            data['d16'].insert(0, isGreaterThan(unita.d16, upperLimit))
            data['d17'].insert(0, isGreaterThan(unita.d17, upperLimit))
            data['d18'].insert(0, isGreaterThan(unita.d18, upperLimit))
            data['d19'].insert(0, isGreaterThan(unita.d19, upperLimit))
            data['d20'].insert(0, isGreaterThan(unita.d20, upperLimit))
            data['d21'].insert(0, isGreaterThan(unita.d21, upperLimit))
            data['d22'].insert(0, isGreaterThan(unita.d22, upperLimit))
            data['d23'].insert(0, isGreaterThan(unita.d23, upperLimit))
            data['d24'].insert(0, isGreaterThan(unita.d24, upperLimit))
            data['d25'].insert(0, isGreaterThan(unita.d25, upperLimit))
            data['d26'].insert(0, isGreaterThan(unita.d26, upperLimit))
            data['d27'].insert(0, isGreaterThan(unita.d27, upperLimit))
            data['d28'].insert(0, isGreaterThan(unita.d28, upperLimit))
            data['d29'].insert(0, isGreaterThan(unita.d29, upperLimit))
            data['d30'].insert(0, isGreaterThan(unita.d30, upperLimit))
            data['d31'].insert(0, isGreaterThan(unita.d31, upperLimit))
            data['d32'].insert(0, isGreaterThan(unita.d32, upperLimit))
            data['d33'].insert(0, isGreaterThan(unita.d33, upperLimit))
            data['d34'].insert(0, isGreaterThan(unita.d34, upperLimit))
            data['d35'].insert(0, isGreaterThan(unita.d35, upperLimit))
            data['d36'].insert(0, isGreaterThan(unita.d36, upperLimit))
            data['d37'].insert(0, isGreaterThan(unita.d37, upperLimit))
            data['d38'].insert(0, isGreaterThan(unita.d38, upperLimit))
            data['d39'].insert(0, isGreaterThan(unita.d39, upperLimit))
            data['d40'].insert(0, isGreaterThan(unita.d40, upperLimit))
            data['d41'].insert(0, isGreaterThan(unita.d41, upperLimit))
            data['d42'].insert(0, isGreaterThan(unita.d42, upperLimit))
            data['d43'].insert(0, isGreaterThan(unita.d43, upperLimit))



        ############ GRAPH ############
        apsdet = "apsdet"


        chartAps = {"type": "heatmap",
                     "marginTop": 40,
                     "marginBottom": 80,
                     "plotBorderWidth": 1,
                     "renderTo": apsdet, "height": 500, }
        titleAps = {"text": 'APS UBI'}
        xAxisAps = {"title": {"text": 'Time'}, "categories": data['IDaps'], }
        yAxisAps = {
            "title": {"text": 'Particule size'},
            "categories": ['<0.523', '0.542', '0.583', '0.626', '0.723', '0.777', '0.835', '0.898', '0.965', '1.037',
                           '1.114', '1.197', '1.286', '1.382', '1;486', '1.596', '1.715', '1.843', '1.981', '2.129',
                           '2.288', '2.458', '2.642', '2.839', '3.051', '3.278', '3.523', '3.786', '4.068', '4.371',
                           '4.698', '5.048', '5.425', '5.829', '6.264', '6.732', '7.234', '7.774', '8.354', '8.977',
                           '9.647', '10.37', '11.14'],
            # 'type': 'logarithmic', #precise logarithmic scale define upper limit
        }

        try:
            Ddayaps = {"text": data["dayaps"][0] + " - " + data["dayaps"][-1], "verticalAlign": 'bottom',
                       "align": 'right'}
        except IndexError:
            Ddayaps = {"text": "Try again, no value", "verticalAlign": 'bottom', "align": 'right'}
            titleAps = {"text": 'NO VALUES'}

        try:
            context['titleday'] = data["dayaps"][0] + " - " + data["dayaps"][-1]
        except IndexError:
            context['titleday'] = datetime(year=start_year, month=start_month, day=start_day)

        context['dateTimeDD'] = datetime(year=start_year, month=start_month, day=start_day)

        context['datatest1']= data['d1']
        context['datatest2']= data['d2']
        context['datatest3']= data['d3']
        context['datatest4']= data['d4']
        context['datatest5']= data['d5']
        context['datatest6']= data['d6']
        context['datatest7']= data['d7']
        context['datatest8']= data['d8']
        context['datatest9']= data['d9']
        context['datatest10'] = data['d10']
        context['datatest11'] = data['d11']
        context['datatest12'] = data['d12']
        context['datatest13'] = data['d13']
        context['datatest14'] = data['d14']
        context['datatest15'] = data['d15']
        context['datatest16'] = data['d16']
        context['datatest17'] = data['d17']
        context['datatest18'] = data['d18']
        context['datatest19'] = data['d19']
        context['datatest20'] = data['d20']
        context['datatest21'] = data['d21']
        context['datatest22'] = data['d22']
        context['datatest23'] = data['d23']
        context['datatest24'] = data['d24']
        context['datatest25'] = data['d25']
        context['datatest26'] = data['d26']
        context['datatest27'] = data['d27']
        context['datatest28'] = data['d28']
        context['datatest29'] = data['d29']
        context['datatest30'] = data['d30']
        context['datatest31'] = data['d31']
        context['datatest32'] = data['d32']
        context['datatest33'] = data['d33']
        context['datatest34'] = data['d34']
        context['datatest35'] = data['d35']
        context['datatest36'] = data['d36']
        context['datatest37'] = data['d37']
        context['datatest38'] = data['d38']
        context['datatest39'] = data['d39']
        context['datatest40'] = data['d40']
        context['datatest41'] = data['d41']
        context['datatest42'] = data['d42']
        context['datatest43'] = data['d43']

        # add the data to the context to send it to the html

        context['apsdet'] = apsdet
        context['chartAps'] = chartAps
        # context['seriesAps'] = seriesAps
        context['title'] = titleAps
        context['xAxis'] = xAxisAps
        context['yAxis'] = yAxisAps
        context['Ddayaps'] = Ddayaps

        context['apsdisplay_det'] = apsdisplay_det


        context['dayaps'] = data['dayaps']


        context['IDaps'] = data['IDaps']
        context['dayaps'] = data['dayaps']


    return render(request, 'data_det/aps.html', context)

def psap_det(request):

    context = {}
    form = DateForm()
    context['form'] = form
    data = {'IDpsap': [], 'blue': [], 'red': [], 'green': [], 'daypsap': [],}



    if request.GET:

        # WORKING :
        start_year = int(request.GET['start_year'])
        start_month = int(request.GET['start_month'])
        start_day = int(request.GET['start_day'])


        try:
            dt = datetime(year=start_year, month=start_month, day=start_day)
        except ValueError:
            return render(request, 'data_det/psap.html', context)
        value = int(time.mktime(dt.timetuple()))
        value = int(value / 10000)
        finishby = 50000
        psapdisplay_det = psap.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value,time__iendswith=finishby)
        print("psapdisplay_det", psapdisplay_det)

        # value = value + 1
        # psapdisplay_det1 = psap.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value,
        #                                                                           time__iendswith=finishby)
        #
        # value = value + 1
        # psapdisplay_det2 = psap.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value,
        #                                                                           time__iendswith=finishby)
        #
        # value = value + 1
        # psapdisplay_det3 = psap.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value,
        #                                                                           time__iendswith=finishby)
        #
        # value = value + 1
        # psapdisplay_det4 = psap.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value,
        #                                                                           time__iendswith=finishby)
        #
        # value = value + 1
        # psapdisplay_det5 = psap.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value,
        #                                                                           time__iendswith=finishby)
        #
        # value = value + 1
        # psapdisplay_det6 = psap.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value,
        #                                                                           time__iendswith=finishby)
        #
        # value = value + 1
        # psapdisplay_det7 = psap.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value,
        #                                                                           time__iendswith=finishby)
        #
        # value = value + 1
        # psapdisplay_det8 = psap.objects.using('dataGOA').order_by('-time').filter(time__istartswith=value,
        #                                                                           time__iendswith=finishby)
        #
        # for unites in psapdisplay_det8:
        #     data['IDpsap'].insert(0, datetime.fromtimestamp(unites.time / 1000).strftime(
        #         "%H:%M"))  # https://www.codegrepper.com/code-examples/python/get+every+nth+element+in+list+python
        #     data['daypsap'].insert(0, datetime.fromtimestamp(unites.time / 1000).strftime("%Y/%m/%d"))
        #     data['blue'].insert(0, unites.blue)
        #     data['red'].insert(0, unites.red)
        #     data['green'].insert(0, unites.green)
        #
        # for unites in psapdisplay_det7:
        #     data['IDpsap'].insert(0, datetime.fromtimestamp(unites.time / 1000).strftime(
        #         "%H:%M"))  # https://www.codegrepper.com/code-examples/python/get+every+nth+element+in+list+python
        #     data['daypsap'].insert(0, datetime.fromtimestamp(unites.time / 1000).strftime("%Y/%m/%d"))
        #     data['blue'].insert(0, unites.blue)
        #     data['red'].insert(0, unites.red)
        #     data['green'].insert(0, unites.green)
        #
        # for unites in psapdisplay_det6:
        #     data['IDpsap'].insert(0, datetime.fromtimestamp(unites.time / 1000).strftime(
        #         "%H:%M"))  # https://www.codegrepper.com/code-examples/python/get+every+nth+element+in+list+python
        #     data['daypsap'].insert(0, datetime.fromtimestamp(unites.time / 1000).strftime("%Y/%m/%d"))
        #     data['blue'].insert(0, unites.blue)
        #     data['red'].insert(0, unites.red)
        #     data['green'].insert(0, unites.green)
        #
        # for unites in psapdisplay_det5:
        #     data['IDpsap'].insert(0, datetime.fromtimestamp(unites.time / 1000).strftime(
        #         "%H:%M"))  # https://www.codegrepper.com/code-examples/python/get+every+nth+element+in+list+python
        #     data['daypsap'].insert(0, datetime.fromtimestamp(unites.time / 1000).strftime("%Y/%m/%d"))
        #     data['blue'].insert(0, unites.blue)
        #     data['red'].insert(0, unites.red)
        #     data['green'].insert(0, unites.green)
        #
        # for unites in psapdisplay_det4:
        #     data['IDpsap'].insert(0, datetime.fromtimestamp(unites.time / 1000).strftime(
        #         "%H:%M"))  # https://www.codegrepper.com/code-examples/python/get+every+nth+element+in+list+python
        #     data['daypsap'].insert(0, datetime.fromtimestamp(unites.time / 1000).strftime("%Y/%m/%d"))
        #     data['blue'].insert(0, unites.blue)
        #     data['red'].insert(0, unites.red)
        #     data['green'].insert(0, unites.green)
        #
        # for unites in psapdisplay_det3:
        #     data['IDpsap'].insert(0, datetime.fromtimestamp(unites.time / 1000).strftime(
        #         "%H:%M"))  # https://www.codegrepper.com/code-examples/python/get+every+nth+element+in+list+python
        #     data['daypsap'].insert(0, datetime.fromtimestamp(unites.time / 1000).strftime("%Y/%m/%d"))
        #     data['blue'].insert(0, unites.blue)
        #     data['red'].insert(0, unites.red)
        #     data['green'].insert(0, unites.green)
        #
        # for unites in psapdisplay_det2:
        #     data['IDpsap'].insert(0, datetime.fromtimestamp(unites.time / 1000).strftime(
        #         "%H:%M"))  # https://www.codegrepper.com/code-examples/python/get+every+nth+element+in+list+python
        #     data['daypsap'].insert(0, datetime.fromtimestamp(unites.time / 1000).strftime("%Y/%m/%d"))
        #     data['blue'].insert(0, unites.blue)
        #     data['red'].insert(0, unites.red)
        #     data['green'].insert(0, unites.green)
        #
        # for unites in psapdisplay_det1:
        #     data['IDpsap'].insert(0, datetime.fromtimestamp(unites.time / 1000).strftime("%H:%M"))  # https://www.codegrepper.com/code-examples/python/get+every+nth+element+in+list+python
        #     data['daypsap'].insert(0, datetime.fromtimestamp(unites.time / 1000).strftime("%Y/%m/%d"))
        #     data['blue'].insert(0, unites.blue)
        #     data['red'].insert(0, unites.red)
        #     data['green'].insert(0, unites.green)

        for unites in psapdisplay_det:
            data['IDpsap'].insert(0, datetime.fromtimestamp(unites.time / 1000).strftime("%H:%M:%S"))  # https://www.codegrepper.com/code-examples/python/get+every+nth+element+in+list+python
            data['daypsap'].insert(0, datetime.fromtimestamp(unites.time / 1000).strftime("%Y/%m/%d"))
            data['blue'].insert(0, unites.blue)
            data['red'].insert(0, unites.red)
            data['green'].insert(0, unites.green)


        ############ GRAPH ############
        psapdet = "psapdet"

        chartPsap = {"renderTo": psapdet, "type": "line", "height": 500, }
        titlePsap = {"text": 'PSAP UBI'}
        xAxisPsap = {"title": {"text": 'Time'}, "categories": data['IDpsap']}
        yAxisPsap = [{"title": {"text": 'σ<sub>a</sub>/Mm<sup>-1</sup>'}}]
        seriesPsap = [
            {"name": 'Blue', "data": data['blue'], "color": "#333fff"},
            {"name": 'Red', "data": data['red'], "color": "#ff3333"},
            {"name": 'Green', "data": data['green'], "color": "#33ff49"},

        ]
        try:
            Ddaypsap = {"text": data["daypsap"][0] + " - " + data["daypsap"][-1], "verticalAlign": 'bottom',
                   "align": 'right'}
        except IndexError:
            Ddaypsap = {"text": "Try again, no value", "verticalAlign": 'bottom', "align": 'right'}
            titlePsap = {"text": 'NO VALUES'}

        # add the data to the context to send it to the html
        try:
            context['titleday'] = data["daypsap"][0] + " - " + data["daypsap"][-1]
        except IndexError:
            context['titleday'] = datetime(year=start_year, month=start_month, day=start_day)

        context['dateTimeDD'] = datetime(year=start_year, month=start_month, day=start_day)

        context['psapdet'] = psapdet
        context['chart'] = chartPsap
        context['seriesPsap'] = seriesPsap
        context['title'] = titlePsap
        context['xAxis'] = xAxisPsap
        context['yAxis'] = yAxisPsap
        context['Ddaypsap'] = Ddaypsap

        context['psapdisplay_det'] = psapdisplay_det
        context['daypsap'] = data['daypsap']



        context['IDpsap'] = data['IDpsap']
        context['daypsap'] = data['daypsap']
        context['blue'] = data['blue']
        context['red'] = data['red']
        context['green'] = data['green']


    return render(request, 'data_det/psap.html', context)

# def demo(request):
#     results = test_calendar()
#     context = {"results": results}
#     return render(request, 'demo.html', context)



# INTRANET

def GOAUVa_Station_SOP(request):
    context = {}
    return render(request, 'intranet_det/SOPs/GOA-UVa-Station-SOP.html', context)

def Neph_SOP(request):
    context = {}
    return render(request, 'intranet_det/SOPs/Neph-SOP.html', context)
def APS_SOP(request):
    context = {}
    return render(request, 'intranet_det/SOPs/APS_SOP.html', context)
def CPC_SOP(request):
    context = {}
    return render(request, 'intranet_det/SOPs/CPC-SOP.html', context)
def PSAP_SOP(request):
    context = {}
    return render(request, 'intranet_det/SOPs/PSAP-SOP.html', context)



def show_Gilib(request):
    filepath = os.path.join('static', 'intranet/Gilib-2_850190M-H.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def show_HMT330(request):
    filepath = os.path.join('static', 'intranet/HMT330 User Guide in English.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def show_HTWC(request):
    filepath = os.path.join('static', 'intranet/HTWC_Series.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def show_M1046(request):
    filepath = os.path.join('static', 'intranet/M1046.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def show_WMR928NX(request):
    filepath = os.path.join('static', 'intranet/WMR928NX.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def show_MANUAL000000300(request):
    filepath = os.path.join('static', 'intranet/MANUAL000000300.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def show_p172401_en(request):
    filepath = os.path.join('static', 'intranet/p172401_en.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def show_dcs910(request):
    filepath = os.path.join('static', 'intranet/dcs910.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def show_J2H20(request):
    filepath = os.path.join('static', 'intranet/J2H20.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def show_MR300(request):
    filepath = os.path.join('static', 'intranet/MR300.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def show_Seco_SV_1003(request):
    filepath = os.path.join('static', 'intranet/Seco-SV-1003-D.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def show_3828A28001B_MANUAL_OWNERS(request):
    filepath = os.path.join('static', 'intranet/3828A28001B_MANUAL_OWNERS.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def show_td_ecowatt_fid4578(request):
    filepath = os.path.join('static', 'intranet/td_ecowatt_fid4578.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def show_J3C_Catalogue_WebRev9(request):
    filepath = os.path.join('static', 'intranet/J3C-Catalogue-WebRev9.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def show_MS_02_346(request):
    filepath = os.path.join('static', 'intranet/MS-02-346.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def show_KNF003_EN(request):
    filepath = os.path.join('static', 'intranet/KNF003_EN.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def show_MuB_el_Stellantrieb_Serie_J3_J3C_en(request):
    filepath = os.path.join('static', 'intranet/MuB_el_Stellantrieb_Serie_J3_J3C_en.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def show_2000_esp(request):
    filepath = os.path.join('static', 'intranet/2000_esp.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def show_00000038(request):
    filepath = os.path.join('static', 'intranet/00000038.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
def show_MI_2000_rev2(request):
    filepath = os.path.join('static', 'intranet/MI_2000_rev2.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')


def PSAPacquire(request):
    context = {}
    return render(request, 'intranet_det/Software/PSAPacquire.html', context)
def VAISALAacquire(request):
    context = {}
    return render(request, 'intranet_det/Software/VAISALAacquire.html', context)

def rsync_webcam(request):
    context = {}
    return render(request, 'intranet_det/Software/rsync_webcam.html', context)
def save_webcam(request):
    context = {}
    return render(request, 'intranet_det/Software/save_webcam.html', context)

def rsync_laptop(request):
    context = {}
    return render(request, 'intranet_det/Software/rsync_laptop.html', context)
def rsync_rawData(request):
    context = {}
    return render(request, 'intranet_det/Software/rsync_rawData.html', context)






def downSampling():
    context = {}
    form = DateForm()
    context['form'] = form
    data = {'IDpsap': [], 'daypsap': [], 'blue': [], 'red': [], 'green': [], 'newblue': [], 'newred': [], 'newgreen': [],'newIDpsap': [], 'newdaypsap': [],}
    x=0
    while x < 75555:

        psapdisplay_det = psap.objects.using('dataGOA').order_by('-time')[x:x+100]

        for unit in psapdisplay_det :
            data['blue'].insert(0, unit.blue)
            data['red'].insert(0, unit.red)
            data['green'].insert(0, unit.green)

            data['IDpsap'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%H:%M"))
            data['daypsap'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%Y/%m/%d"))

        # print(data['blue'], data['red'], data['green'])

        avgBlue = sum(data['blue']) / len(data['blue'])
        avgRed = sum(data['red']) / len(data['red'])
        avgGreen = sum(data['green']) / len(data['green'])

        data['newblue'].insert(0, avgBlue)
        data['newred'].insert(0, avgRed)
        data['newgreen'].insert(0, avgGreen)

        data['newIDpsap'].insert(0,data['IDpsap'][0])
        data['newdaypsap'].insert(0,data['daypsap'][0])

        # print('blue',avgBlue, 'red', avgRed, 'green', avgGreen)

        x = x + 100

    print('out blue', data['newblue'], 'red', data['newred'], 'green', data['newgreen'], 'time', data['newIDpsap'])

    return avgBlue, avgRed, avgGreen

        # if new_time == previous_time :
        #
        #     break

        # downSampling()


def APSdownSampling():
    context = {}
    form = DateForm()
    context['form'] = form
    data = {
        'IDaps': [],'dayaps': [],
        'd1': [],'d2': [], 'd3': [], 'd4': [],'d5': [],'d6': [],'d7': [],'d8': [],'d9': [],'d10': [],
        'd11': [],'d12': [], 'd13': [], 'd14': [],'d15': [],'d16': [],'d17': [],'d18': [],'d19': [],'d20': [],
        'd21': [],'d22': [], 'd23': [], 'd24': [],'d25': [],'d26': [],'d27': [],'d28': [],'d29': [],'d30': [],
        'd31': [],'d32': [], 'd33': [], 'd34': [],'d35': [],'d36': [],'d37': [],'d38': [],'d39': [],'d40': [],
        'd41': [],'d42': [], 'd43':[],
        'newIDaps': [], 'newdayaps': [],
        'newd1': [],'newd2': [], 'newd3': [], 'newd4': [],'newd5': [],'newd6': [],'newd7': [],'newd8': [],'newd9': [],'newd10': [],
        'newd11': [],'newd12': [], 'newd13': [], 'newd14': [],'newd15': [],'newd16': [],'newd17': [],'newd18': [],'newd19': [],'newd20': [],
        'newd21': [],'newd22': [], 'newd23': [], 'newd24': [],'newd25': [],'newd26': [],'newd27': [],'newd28': [],'newd29': [],'newd30': [],
        'newd31': [],'newd32': [], 'newd33': [], 'newd34': [],'newd35': [],'newd36': [],'newd37': [],'newd38': [],'newd39': [],'newd40': [],
        'newd41': [],'newd42': [], 'newd43':[],
            }
    y=0
    while y < 235:

        apses = aps.objects.using('dataGOA').order_by('-time')[x:x+5]
        # print(apses)


        upperLimit = 600

        for unita in apses:
            data['IDaps'].insert(0, datetime.fromtimestamp(unita.time / 1000).strftime("%H:%M"))
            data['dayaps'].insert(0, datetime.fromtimestamp(unita.time / 1000).strftime("%Y/%m/%d"))
            data['d1'].insert(0, unita.d1)
            data['d2'].insert(0, unita.d2)
            data['d3'].insert(0, unita.d3)
            data['d4'].insert(0, unita.d4)
            data['d5'].insert(0, unita.d5)
            data['d6'].insert(0, unita.d6)
            data['d7'].insert(0, unita.d7)
            data['d8'].insert(0, unita.d8)
            data['d9'].insert(0, unita.d9)
            data['d10'].insert(0, unita.d10)
            data['d11'].insert(0, unita.d11)
            data['d12'].insert(0, unita.d12)
            data['d13'].insert(0, unita.d13)
            data['d14'].insert(0, unita.d14)
            data['d15'].insert(0, unita.d15)
            data['d16'].insert(0, unita.d16)
            data['d17'].insert(0, unita.d17)
            data['d18'].insert(0, unita.d18)
            data['d19'].insert(0, unita.d19)
            data['d20'].insert(0, unita.d20)
            data['d21'].insert(0, unita.d21)
            data['d22'].insert(0, unita.d22)
            data['d23'].insert(0, unita.d23)
            data['d24'].insert(0, unita.d24)
            data['d25'].insert(0, unita.d25)
            data['d26'].insert(0, unita.d26)
            data['d27'].insert(0, unita.d27)
            data['d28'].insert(0, unita.d28)
            data['d29'].insert(0, unita.d29)
            data['d30'].insert(0, unita.d30)
            data['d31'].insert(0, unita.d31)
            data['d32'].insert(0, unita.d32)
            data['d33'].insert(0, unita.d33)
            data['d34'].insert(0, unita.d34)
            data['d35'].insert(0, unita.d35)
            data['d36'].insert(0, unita.d36)
            data['d37'].insert(0, unita.d37)
            data['d38'].insert(0, unita.d38)
            data['d39'].insert(0, unita.d39)
            data['d40'].insert(0, unita.d40)
            data['d41'].insert(0, unita.d41)
            data['d42'].insert(0, unita.d42)
            data['d43'].insert(0, unita.d43)


        avgd1 = sum(data['d1']) / len(data['d1'])
        avgd2 = sum(data['d2']) / len(data['d2'])
        avgd3 = sum(data['d3']) / len(data['d3'])
        avgd4 = sum(data['d4']) / len(data['d4'])
        avgd5 = sum(data['d5']) / len(data['d5'])
        avgd6 = sum(data['d6']) / len(data['d6'])
        avgd7 = sum(data['d7']) / len(data['d7'])
        avgd8 = sum(data['d8']) / len(data['d8'])
        avgd9 = sum(data['d9']) / len(data['d9'])
        avgd10 = sum(data['d10']) / len(data['d10'])
        avgd11 = sum(data['d11']) / len(data['d11'])
        avgd12 = sum(data['d12']) / len(data['d12'])
        avgd13 = sum(data['d13']) / len(data['d13'])
        avgd14 = sum(data['d14']) / len(data['d14'])
        avgd15 = sum(data['d15']) / len(data['d15'])
        avgd16 = sum(data['d16']) / len(data['d16'])
        avgd17 = sum(data['d17']) / len(data['d17'])
        avgd18 = sum(data['d18']) / len(data['d18'])
        avgd19 = sum(data['d19']) / len(data['d19'])
        avgd20 = sum(data['d20']) / len(data['d20'])
        avgd21 = sum(data['d21']) / len(data['d21'])
        avgd22 = sum(data['d22']) / len(data['d22'])
        avgd23 = sum(data['d23']) / len(data['d23'])
        avgd24 = sum(data['d24']) / len(data['d24'])
        avgd25 = sum(data['d25']) / len(data['d25'])
        avgd26 = sum(data['d26']) / len(data['d26'])
        avgd27 = sum(data['d27']) / len(data['d27'])
        avgd28 = sum(data['d28']) / len(data['d28'])
        avgd29 = sum(data['d29']) / len(data['d29'])
        avgd30 = sum(data['d30']) / len(data['d30'])
        avgd31 = sum(data['d31']) / len(data['d31'])
        avgd32 = sum(data['d32']) / len(data['d32'])
        avgd33 = sum(data['d33']) / len(data['d33'])
        avgd34 = sum(data['d34']) / len(data['d34'])
        avgd35 = sum(data['d35']) / len(data['d35'])
        avgd36 = sum(data['d36']) / len(data['d36'])
        avgd37 = sum(data['d37']) / len(data['d37'])
        avgd38 = sum(data['d38']) / len(data['d38'])
        avgd39 = sum(data['d39']) / len(data['d39'])
        avgd40 = sum(data['d40']) / len(data['d40'])
        avgd41 = sum(data['d41']) / len(data['d41'])
        avgd42 = sum(data['d42']) / len(data['d42'])
        avgd43 = sum(data['d43']) / len(data['d43'])


        data['newd1'].insert(0, isGreaterThan(avgd1, upperLimit))
        data['newd2'].insert(0, isGreaterThan(avgd2, upperLimit))
        data['newd3'].insert(0, isGreaterThan(avgd3, upperLimit))
        data['newd4'].insert(0, isGreaterThan(avgd4, upperLimit))
        data['newd5'].insert(0, isGreaterThan(avgd5, upperLimit))
        data['newd6'].insert(0, isGreaterThan(avgd6, upperLimit))
        data['newd7'].insert(0, isGreaterThan(avgd7, upperLimit))
        data['newd8'].insert(0, isGreaterThan(avgd8, upperLimit))
        data['newd9'].insert(0, isGreaterThan(avgd9, upperLimit))
        data['newd10'].insert(0, isGreaterThan(avgd10, upperLimit))
        data['newd11'].insert(0, isGreaterThan(avgd11, upperLimit))
        data['newd12'].insert(0, isGreaterThan(avgd12, upperLimit))
        data['newd13'].insert(0, isGreaterThan(avgd13, upperLimit))
        data['newd14'].insert(0, isGreaterThan(avgd14, upperLimit))
        data['newd15'].insert(0, isGreaterThan(avgd15, upperLimit))
        data['newd16'].insert(0, isGreaterThan(avgd16, upperLimit))
        data['newd17'].insert(0, isGreaterThan(avgd17, upperLimit))
        data['newd18'].insert(0, isGreaterThan(avgd18, upperLimit))
        data['newd19'].insert(0, isGreaterThan(avgd19, upperLimit))
        data['newd20'].insert(0, isGreaterThan(avgd20, upperLimit))
        data['newd21'].insert(0, isGreaterThan(avgd21, upperLimit))
        data['newd22'].insert(0, isGreaterThan(avgd22, upperLimit))
        data['newd23'].insert(0, isGreaterThan(avgd23, upperLimit))
        data['newd24'].insert(0, isGreaterThan(avgd24, upperLimit))
        data['newd25'].insert(0, isGreaterThan(avgd25, upperLimit))
        data['newd26'].insert(0, isGreaterThan(avgd26, upperLimit))
        data['newd27'].insert(0, isGreaterThan(avgd27, upperLimit))
        data['newd28'].insert(0, isGreaterThan(avgd28, upperLimit))
        data['newd29'].insert(0, isGreaterThan(avgd29, upperLimit))
        data['newd30'].insert(0, isGreaterThan(avgd30, upperLimit))
        data['newd31'].insert(0, isGreaterThan(avgd31, upperLimit))
        data['newd32'].insert(0, isGreaterThan(avgd32, upperLimit))
        data['newd33'].insert(0, isGreaterThan(avgd33, upperLimit))
        data['newd34'].insert(0, isGreaterThan(avgd34, upperLimit))
        data['newd35'].insert(0, isGreaterThan(avgd35, upperLimit))
        data['newd36'].insert(0, isGreaterThan(avgd36, upperLimit))
        data['newd37'].insert(0, isGreaterThan(avgd37, upperLimit))
        data['newd38'].insert(0, isGreaterThan(avgd38, upperLimit))
        data['newd39'].insert(0, isGreaterThan(avgd39, upperLimit))
        data['newd40'].insert(0, isGreaterThan(avgd40, upperLimit))
        data['newd41'].insert(0, isGreaterThan(avgd41, upperLimit))
        data['newd42'].insert(0, isGreaterThan(avgd42, upperLimit))
        data['newd43'].insert(0, isGreaterThan(avgd43, upperLimit))


        print(data['newd1'])



        data['newIDaps'].insert(0,data['IDaps'][0])
        data['newdayaps'].insert(0,data['dayaps'][0])

        # print('blue',avgBlue, 'red', avgRed, 'green', avgGreen)

        y = y + 5

    print('newD1', data['newd1'], 'time', data['newIDaps'],'newD33', data['newd33'],'newD24', data['newd24'],)

    return 0



# .raw('''SELECT *
#    FROM (
#        SELECT
#            @row := @row +1 AS rownum, time
#        FROM (
#            SELECT @row :=0) r, PSAP_UBI
#        ) ranked
#    WHERE rownum % 5 = 1 ''')



import mysql.connector

def downSampling3():


    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="goaubi"
    )

    mycursor = mydb.cursor()

    # Preparing the query to delete records
    sql = "TRUNCATE TABLE newpsap"

    try:
        # Execute the SQL command
        mycursor.execute(sql)

        # Commit your changes in the database
        mydb.commit()
    except:
        # Roll back in case there is any error
        mydb.rollback()



    data = {'IDpsap': [], 'daypsap': [], 'blue': [], 'red': [], 'green': [], 'newblue': [], 'newred': [],
            'newgreen': [], 'newIDpsap': [], 'newdaypsap': [], }

    psapdisplay_det3 = psap.objects.using('dataGOA').order_by('-time')[:50000]


    for unit in psapdisplay_det3:
        data['IDpsap'].insert(0, unit.time)
        data['blue'].insert(0, unit.blue)
        data['red'].insert(0, unit.red)
        data['green'].insert(0, unit.green)
        # data['IDpsap'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%H:%M"))
        # data['daypsap'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%Y/%m/%d"))

    i=0
    while i < len(data['blue']):
        tim =  data['IDpsap'][i]
        blue100 = data['blue'][i:i+99]
        newblue = sum(blue100)/len(blue100)

        red100 = data['red'][i:i + 99]
        newred = sum(red100) / len(red100)

        green100 = data['green'][i:i + 99]
        newgreen = sum(green100) / len(green100)

        # data['newblue'].insert(0, newblue)


        print("t=",tim )
        sql = "INSERT INTO newpsap (time, blue, red, green) VALUES (%s, %s, %s, %s)"

        val = (tim, newblue, newred, newgreen)

        mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "record inserted.")

        i += 100
    # print(data['newblue'])
    return data
