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
