import urllib.request
import xml.etree.ElementTree as ET
import requests


class NEAweather:
    def __init__(self,config):
        self.APIkey = config['NEA']['key']

    def get_PSI(self):
        uri = 'http://www.nea.gov.sg/'
        path = 'api/WebAPI/?dataset='

        datasetName=['psi_update','pm2.5_update']

        url_psi = uri + path + datasetName[0] + '&keyref=' + self.APIkey
        url_pm25 = uri + path + datasetName[1] + '&keyref=' + self.APIkey

        r_psi = urllib.request.urlopen(url_psi)
        print(r_psi)
        tree_psi = ET.parse(r_psi)
        root_psi = tree_psi.getroot()

        r_pm25 = urllib.request.urlopen(url_pm25)
        print (r_pm25)
        tree_pm25 =ET.parse(r_pm25)
        root_pm25 = tree_pm25.getroot()
        PSI = {}
        PSI['psi'] = root_psi[2][2][3][1].attrib['value']
        PSI['pm2.5'] = root_pm25[2][2][3][0].attrib['value']

        return PSI

class YAHOOweather:
    def __init__(self):
        pass

    def code_lookup(self,code):
        codeDict ={}
        codeDict['0'] = 'tornado'
        codeDict['1'] = 'tropical storm'
        codeDict['2'] = 'hurricane'
        codeDict['3'] = 'severe thunderstorms'
        codeDict['4'] = 'mixed rain and snow'
        codeDict['5'] = 'mixed rain and sleet'
        codeDict['6'] = 'mixed snow and sleet'
        codeDict['7'] = 'hurricane'
        codeDict['8'] = 'freezing drizzle'
        codeDict['9'] = 'drizzle'
        codeDict['10'] = 'freezing rain'
        codeDict['11'] = 'showers'
        codeDict['12'] = 'showers'
        codeDict['13'] = 'snow flurries'
        codeDict['14'] = 'light snow showers'
        codeDict['15'] = 'blowing snow'
        codeDict['16'] = 'snow'
        codeDict['17'] = 'hail'
        codeDict['18'] = 'sleet'
        codeDict['19'] = 'dust'
        codeDict['20'] = 'foggy'
        codeDict['21'] = 'haze'
        codeDict['22'] = 'smoky'
        codeDict['23'] = 'blustery'
        codeDict['24'] = 'windy'
        codeDict['25'] = 'cold'
        codeDict['26'] = 'cloudy'
        codeDict['27'] = 'mostly cloudy (night)'
        codeDict['28'] = 'mostly cloudy (day)'
        codeDict['29'] = 'partly cloudy (night)'
        codeDict['30'] = 'partly cloudy (day)'
        codeDict['31'] = 'clear (night)'
        codeDict['32'] = 'sunny'
        codeDict['33'] = 'fair (night)'
        codeDict['34'] = 'fair (day)'
        codeDict['35'] = 'mixed rain and hail'
        codeDict['36'] = 'hot'
        codeDict['37'] = 'isolated thunderstorms'
        codeDict['38'] = 'scattered thunderstorms'
        codeDict['39'] = 'scattered thunderstorms'
        codeDict['40'] = 'scattered showers'
        codeDict['41'] = 'heavy snow'
        codeDict['42'] = 'scattered snow showers'
        codeDict['43'] = 'heavy snow'
        codeDict['44'] = 'partly cloudy'
        codeDict['45'] = 'thundershowers'
        codeDict['46'] = 'snow showers'
        codeDict['47'] = 'isolated thundershowers'
        codeDict['3200'] = 'not available'

        if code in codeDict:
            return codeDict[code]
        else:
            return 'incorrect code'

    def get_weather(self):

        uri = 'https://query.yahooapis.com/'
        path = 'v1/public/yql?'
        format = '&format=json'
        YQL = ("q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22Bedok%2C%20Singapore%22)%20and%20u%3D'c'")

        url = uri + path + YQL + format

        r = requests.get(url)
        j = r.json()

        weatherdata = {}
        weatherdata['pubDate'] = j['query']['results']['channel']['item']['pubDate']
        weatherdata['humidity'] = j['query']['results']['channel']['atmosphere']['humidity'] + '%'
        weatherdata['pressure'] = j['query']['results']['channel']['atmosphere']['pressure'] + 'mbar'
        weatherdata['sunrise'] = j['query']['results']['channel']['astronomy']['sunrise']
        weatherdata['sunset'] = j['query']['results']['channel']['astronomy']['sunset']
        weatherdata['currentState'] = self.code_lookup(j['query']['results']['channel']['item']['condition']['code']).title()
        weatherdata['currentTemp'] = j['query']['results']['channel']['item']['condition']['temp'] + '°C'

        return (weatherdata)



