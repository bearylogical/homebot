from flask_restful import Resource, Api

from . import api_module
from .resources.transport import LTA_Transport, googleTransit
from .resources.weather import NEAweather,YAHOOweather, darkskyWeather
import yaml
import os.path

with open(os.path.dirname(__file__) + "/../../config.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile)

api = Api(api_module)

class nextbus(Resource):

    def get(self):
        bus = LTA_Transport(config)
        arrivals = bus.get_timings(str(config['location']['busstop']))
        return arrivals

class transit(Resource):

    def get(self):
        travel = googleTransit(config)
        return travel.get_travelTimes()

class PSI(Resource):
    def get(self):
        psi = NEAweather(config)
        return psi.get_PSI()

class Weather(Resource):
    def get(self):
        weather = darkskyWeather(config)
        return weather.get_forecast()

api.add_resource(nextbus,'/v1/nextbus')
api.add_resource(transit,'/v1/transit')
api.add_resource(Weather,'/v1/weather')
api.add_resource(PSI,'/v1/psi')


#
# @api_module.route('/nextbus')

