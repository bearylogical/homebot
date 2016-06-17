from . import dash



@dash.route('/', methods=['GET'])
def index():
    return dash.send_static_file("index.html")
