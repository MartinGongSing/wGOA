from datetime import datetime
import time

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
import requests
import math


from django.db.models import Count, Q
import json

from django.conf import settings

from models import cpc, instrument, cpc2, neph2, aps, psap, cpc3



def downSampling():
    context = {}
    form = DateForm()
    context['form'] = form
    data = {'IDpsap': [], 'blue': [], 'red': [], 'green': []}
    x=0
    while x<99990:

        psapdisplay_det = psap.objects.order_by('-time')[x:x+10]

        for unit in psapdisplay_det :
            data['blue'].insert(0, unit.blue)
            data['red'].insert(0, unit.red)
            data['green'].insert(0, unit.green)

        avgBlue = sum(data['blue']) / len(data['blue'])
        avgRed = sum(data['red']) / len(data['red'])
        avgGreen = sum(data['green']) / len(data['green'])



        print('blue',avgBlue, 'red', avgRed, 'green', avgGreen)

        x+=10

        return avgBlue, avgRed, avgGreen

        # if new_time == previous_time :
        #
        #     break


downSampling()

