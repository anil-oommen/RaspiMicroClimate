


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

@app.route('/action/<string:arg>')
def pg_string(request, arg):
    print("Processing Request:",request, arg)
    return 'success'


# see http://www.tutorialspoint.com/angular_material/angular_material_radiobuttons.htm
@app.route('/index')
def home(request):
    #https://material.angularjs.org/latest/demo/button
    return File("index2.html")
    #return '<img src="/static/img.gif">'

@app.route('/static/', branch=True)
def static(request):
    return File("./static")

config = initConfig()
ws_port = config.get('AppWSConnector', 'host_port')
app.run("", int(ws_port))