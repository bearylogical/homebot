import requests
import datetime
import math
import json
from collections import OrderedDict


class LTA_Transport:
    def __init__(self, config):
        self.AccountKey = config['LTA']['AccountKey']
        self.UniqueUserID = config['LTA']['UniqueUserID']

    def get_timings(self, BusStopID):
        uri = 'http://datamall2.mytransport.sg/'  # Resource URL
        path = 'ltaodataservice/BusArrival?'

        headers = {'AccountKey': self.AccountKey,
                   'UniqueUserID': self.UniqueUserID,
                   "accept": "application/JSON"}

        url = uri + path
        payload = ('BusStopID=' + BusStopID + '&SST=True')

        r = requests.get(url, headers=headers, params=payload)
        j = r.json()
        busArr = j['Services']
        now = datetime.datetime.now()
        fmt = "%H:%M:%S"

        arrival = []

        for index in range(len(busArr)):
            arrivalTemplate = OrderedDict({
                'Bus': ' ',
                'ArrivalTimes':
                    [
                        {
                            'NextBus': '',
                            'SubsequentBus': '',
                            'SubsequentBus3': ''
                        }
                    ]
            })
            currBus = (busArr[index]['ServiceNo'])
            arrivalTemplate['Bus'] = currBus
            ArrivalTimes = sorted((arrivalTemplate['ArrivalTimes'][0]).keys())
            for t in range(len(ArrivalTimes)):
                descArrival = ArrivalTimes[t]
                estdArrival = ((busArr[index])[descArrival]['EstimatedArrival'])[11:19]
                if (estdArrival):
                    arrivalInterval = math.trunc((datetime.datetime.strptime(estdArrival, fmt) - now).seconds / 60)
                    if (arrivalInterval == 0 or arrivalInterval > 100):
                        (arrivalTemplate['ArrivalTimes'][0][descArrival]) = 'Arr'
                    else:
                        (arrivalTemplate['ArrivalTimes'][0][descArrival]) = str(arrivalInterval) + ' mins'
                else:
                    (arrivalTemplate['ArrivalTimes'][0][descArrival]) = 'N.A.'
            arrival.insert(index, arrivalTemplate)
        return arrival


class googleTransit:
    def __init__(self,config):
        self.APIkey = config['google']['APIkey']

    def get_travelTimes(self,startDest='',endDest=''):
        uri = 'https://maps.googleapis.com/'
        path = 'maps/api/directions/json?'

        if startDest=='' and endDest=='':
            startDest='35 Jalan Tanjong, Singapore 468040'
            endDest='Applied Materials South East Asia Pte Ltd, 8 Upper Changi Road North, Singapore 506906'

        origin = 'origin=' +  startDest.replace(' ','+')
        destination = 'destination=' + endDest.replace(' ','+')
        mode = 'mode=transit'
        key = 'key=' + self.APIkey

        url = uri + path + origin + '&' + destination + '&' + mode + '&' + key

        # print (url)
        r = requests.get(url)
        j = r.json()

        transitData = {}
        transitData['departure_time'] = j['routes'][0]['legs'][0]['departure_time']['text']
        transitData['arrival_time'] = j['routes'][0]['legs'][0]['arrival_time']['text']
        transitData['distance'] = j['routes'][0]['legs'][0]['distance']['text']
        transitData['duration'] = j['routes'][0]['legs'][0]['duration']['text']
        return transitData



