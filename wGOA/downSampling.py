from models import psap
from django.db.models import Count, Q
from django.conf import settings
import os
import math
from datetime import datetime
import time


def downSampling():

    context = {}

    data = {'IDpsap': [], 'daypsap': [], 'blue': [], 'red': [], 'green': [], 'newblue': [], 'newred': [],
            'newgreen': [], 'newIDpsap': [], 'newdaypsap': [], }

    psapdisplay_det = psap.objects.using('dataGOA').order_by('-time')[:1000]


    for unit in psapdisplay_det:
        data['blue'].insert(0, unit.blue)
        # data['red'].insert(0, unit.red)
        # data['green'].insert(0, unit.green)
        # data['IDpsap'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%H:%M"))
        # data['daypsap'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%Y/%m/%d"))

    i=0
    while i < len(data['blue']):
        blue100 = data['blue'][i:i+100]
        data['newblue'] = sum(blue100)/len(blue100)

        i+=100

    print(data['newblue'])
    return data


downSampling()

    #
    # x = 0
    # while x < 75555:
    #
    #     psapdisplay_det = psap.objects.using('dataGOA').order_by('-time')[x:x + 100]
    #
    #     for unit in psapdisplay_det:
    #         data['blue'].insert(0, unit.blue)
    #         data['red'].insert(0, unit.red)
    #         data['green'].insert(0, unit.green)
    #
    #         data['IDpsap'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%H:%M"))
    #         data['daypsap'].insert(0, datetime.fromtimestamp(unit.time / 1000).strftime("%Y/%m/%d"))
    #
    #
    #
    #     avgBlue = sum(data['blue']) / len(data['blue'])
    #     avgRed = sum(data['red']) / len(data['red'])
    #     avgGreen = sum(data['green']) / len(data['green'])
    #
    #     data['newblue'].insert(0, avgBlue)
    #     data['newred'].insert(0, avgRed)
    #     data['newgreen'].insert(0, avgGreen)
    #
    #     data['newIDpsap'].insert(0, data['IDpsap'][0])
    #     data['newdaypsap'].insert(0, data['daypsap'][0])
    #
    #
    #
    #     x = x + 100

########################

        # return render(request, '[TEMPLATE.html]', context)




