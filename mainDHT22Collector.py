import urllib
import urllib.request
#import urllib2
import xml.etree.ElementTree as etree
import threading
import time
import logging
import sys
import Adafruit_DHT


# Local Modules to include
from modWSCommon import webserviceInvokeAction
from modAppConfig import initConfig


humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 23)
if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)


logging.basicConfig(level=logging.DEBUG,
                    format='(%(asctime)s %(levelname)s %(filename)s-%(process)d-%(threadName)-9s) %(message)s',)


def dht22Daemon():
    config = initConfig()
    dht22_poll_interval_minutes = config.get('DHT22Collector', 'dht22_poll_interval_minutes')
    while 1:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 23)
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
            paramDataArray = {}
            paramDataArray['temperature_dc'] = temperature
            paramDataArray['humidity_pc'] = humidity
            webserviceInvokeAction(config, "dht22sensor", paramDataArray)
        else:
            print('Failed to get reading. Try again!')
        logging.info("Sleep for Minutes: " + str(dht22_poll_interval_minutes))
        time.sleep(int(dht22_poll_interval_minutes) * 60)



if __name__ == '__main__':
    wDaemon = threading.Thread(name='daemon', target=dht22Daemon)
    wDaemon.setDaemon(True)
    wDaemon.start()
    wDaemon.join()




