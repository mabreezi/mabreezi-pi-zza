# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import requests
import re

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from hyper.models import Shipment

# Create your views here.

@csrf_exempt
def send_location(request, shipment_number):
    # return HttpResponse('Location Here')
    print 'Location Here'
    body_unicode = request.body.decode('utf-8')
    # body = json.loads(body_unicode)
    # content = body['content']
    print body_unicode

    coordinates = re.compile(r'lat=([\d\.]+)&lon=([\d\.]+)')

    lat, lon = re.search(coordinates, body_unicode).group(1), re.search(coordinates, body_unicode).group(2)

    print lat
    print lon

    shipment = Shipment.objects.get(pk=shipment_number)
    shipment_id = shipment.shipment_id

    # shipment_access_token = ''

    # params = {'access_token' : shipment_access_token}

    # data = {
    # "$class": "org.kibaati.LocationUpdate",
    # "location": "{},{}".format(str(lat), str(lon)),
    # "shipment": "org.kibaati.Shipment#{}".format(shipment_id),
    # }

    # try:
    #     r = requests.post('http://{}/api/LocationUpdate'.format(settings.HYPER_SERVER), data=data, params= params )
    #     if r.status_code / 100 != 2:
    #         raise ValueError('Could not send the location')
    # except ValueError as error:
    #     print ValueError + '\n' + r.text
    #     return HttpResponse(r.text)

    return HttpResponse('Location Here')
