from flask_restful import Resource, Api

from . import api_module
from .resources.transport import LTA_Transport
import yaml
import os.path

with open(os.path.dirname(__file__) + "/../../config.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile)

api = Api(api_module)



class nextbus(Resource):

    def get(self):
        bus = LTA_Transport(config)
        arrivals = bus.get_timings('85091')
        return arrivals

api.add_resource(nextbus,'/v1/nextbus')


#
# @api_module.route('/nextbus')

