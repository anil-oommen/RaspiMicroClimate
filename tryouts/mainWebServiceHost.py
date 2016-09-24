


'''
to install pip and klein

  sudo apt-get install python3-dev


 1920  sudo apt-get install python-pip
 1921  pip or use pip3
 1922
 1924  sudo pip/pip3 install klein
 1924  sudo pip/pip3 install twisted
 1925  history



'''

#from twisted.internet.defer import succeed
#from klein import run, route
from twisted.web.static import File
from klein import Klein
# Local Modules to include when running in Raspberry PI
from modAppConfig import initConfig



app = Klein()





'''

@app.route('/<string:arg>')
def pg_string(request, arg):
    return 'String: %s!' % (arg,)

@app.route('/<float:arg>')
def pg_float(request, arg):
    return 'Float: %s!' % (arg,)

@app.route('/<int:arg>')
def pg_int(request, arg):
    return 'Int: %s!' % (arg,)

'''


@app.route('/rmcapp')
def rmc_app(request, methods=['GET','POST']):
    print("Processing Request 3:",request)
    weather_code = request.args.get('weather_code', [''])[0]
    #weather_code = request.form['weather_code']
    weather_desc = request.args.get('weather_desc', ['NA'])[0]
    weather_location = request.args.get('weather_location', ['NA'])[0]
    print("NEA WeatherData:", weather_code ,weather_desc,  weather_location)
    return 'success' + weather_code + weather_desc + weather_location

'''
@app.route('/rmcapp/<string:arg>')
def rmc_app(request, arg, methods=['GET']):
    print("Processing Request 3:",request)
    weather_code = request.args.get('weather_code', [''])[0]
    #weather_code = request.form['weather_code']
    weather_desc = request.args.get('weather_desc', ['NA'])[0]
    weather_location = request.args.get('weather_location', ['NA'])[0]
    print("NEA WeatherData:", weather_code ,weather_desc,  weather_location)
    return 'success' + weather_code

'''


@app.route('/action/<string:arg>')
def pg_string(request, arg):
    print("Processing Request1:",request, arg)
    name = request.args.get('name', ['world'])[0]
    return 'success'


# see http://www.tutorialspoint.com/angular_material/angular_material_radiobuttons.htm
@app.route('/webapp/index')
def home(request):
    #https://material.angularjs.org/latest/demo/button
    return File("webapp/index.html")
    #return '<img src="/static/img.gif">'

@app.route('/webapp', branch=True)
def static(request):
    return File("webapp")

config = initConfig()
ws_port = config.get('AppWSConnector', 'host_port')
app.run("", int(ws_port))