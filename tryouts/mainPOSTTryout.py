from twisted.internet.defer import succeed
from klein import run, route

name='world'

@route('/', methods=['POST'])
def setname(request):
    global name
    name = request.args.get('name', ['world'])[0]
    request.redirect('/')
    return succeed(None)

@route('/')
def hello(request):
    return "Hello, {0}!".format(name)

run("localhost", 8081)