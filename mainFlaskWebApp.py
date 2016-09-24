#!flask/bin/python
from app import app
from modAppConfig import initConfig

config = initConfig()

app.run(host='0.0.0.0', debug=True, port=config.getint('AppWSConnector', 'host_port'))