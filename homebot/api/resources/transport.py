import requests
import datetime
import math
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
                'Data':
                    [
                        {
                            'NextBus':
                                [
                                    {
                                        'ArrivalTime':'',
                                        'Latitude':'',
                                        'Longitude':''
                                    }
                                ],
                            'SubsequentBus':
                                [
                                    {
                                        'ArrivalTime': '',
                                        'Latitude': '',
                                        'Longitude': ''
                                    }
                                ],

                            'SubsequentBus3':
                                [
                                    {
                                        'ArrivalTime': '',
                                        'Latitude': '',
                                        'Longitude': ''
                                    }
                                ],
                        }
                    ]
            })
            arrivalTemplate['Bus'] = (busArr[index]['ServiceNo'])
            ArrivalTimes = sorted((arrivalTemplate['Data'][0]).keys())
            for t in range(len(ArrivalTimes)):
                descKey = ArrivalTimes[t]
                if ((busArr[index][descKey]['Latitude']) or (busArr[index][descKey]['Latitude'])):
                    arrivalTemplate['Data'][0][descKey][0]['Latitude'] = busArr[index][descKey]['Latitude']
                    arrivalTemplate['Data'][0][descKey][0]['Longitude'] = busArr[index][descKey]['Longitude']
                else:
                    arrivalTemplate['Data'][0][descKey][0]['Latitude'] = 'N.A.'
                    arrivalTemplate['Data'][0][descKey][0]['Longitude'] = 'N.A.'
                estdArrival = ((busArr[index])[descKey]['EstimatedArrival'])[11:19]
                if (estdArrival):
                    arrivalInterval = math.trunc((datetime.datetime.strptime(estdArrival, fmt) - now).seconds / 60)
                    if (arrivalInterval == 0 or arrivalInterval > 100):
                        (arrivalTemplate['Data'][0][descKey][0]['ArrivalTime']) = 'Arr'
                    else:
                        (arrivalTemplate['Data'][0][descKey][0]['ArrivalTime']) = str(arrivalInterval) + ' mins'
                else:
                    (arrivalTemplate['Data'][0][descKey][0]['ArrivalTime']) = 'N.A.'
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
            endDest='Micron Semiconductor Singapore'

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



