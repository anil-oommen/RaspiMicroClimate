import urllib
import urllib.request
#import urllib2
import xml.etree.ElementTree as etree
import threading
import time
import logging


# Local Modules to include
from modWSCommon import webserviceInvokeAction
from modAppConfig import initConfig
from urllib.request import Request, urlopen



logging.basicConfig(level=logging.DEBUG,
                    format='(%(asctime)s %(levelname)s %(filename)s-%(process)d-%(threadName)-9s) %(message)s',)




# Mapping Speclet https://www.nea.gov.sg/docs/default-source/api/developer's-guide.pdf
def mapNEAForcasteCode(fCode):
    if fCode =="HT": return "Heavy Thundery Showers"
    if fCode == "BR": return "Mist"
    if fCode == "CL": return "Cloudy"
    if fCode == "DR": return "Drizzle"
    if fCode == "FA": return "Fair (Day)"
    if fCode == "FG": return "Fog"
    if fCode == "FN": return "Fair (Night)"
    if fCode == "FW": return "Fair & Warm"
    if fCode == "HG": return " Heavy Thundery Showers with Gusty Winds"
    if fCode == "HR": return "Heavy Rain"
    if fCode == "HS": return "Heavy Showers"
    if fCode == "HT": return "Heavy Thundery Showers"
    if fCode == "HZ": return "Hazy"
    if fCode == "LH": return "Slightly Hazy"
    if fCode == "LR": return "Light Rain"
    if fCode == "LS": return "Light Showers"
    if fCode == "OC": return "Overcast"
    if fCode == "PC": return "Partly Cloudy (Day)"
    if fCode == "PN": return "Partly Cloudy (Night)"
    if fCode == "PS": return "Passing Showers"
    if fCode == "RA": return "Moderate Rain"
    if fCode == "SH": return "Showers"
    if fCode == "SK": return "Strong Winds, Showers"
    if fCode == "SN": return "Snow"
    if fCode == "SR": return "Strong Winds, Rain"
    if fCode == "SS": return "Snow Showers"
    if fCode == "SU": return "Sunny"
    if fCode == "SW": return "Strong Winds"
    if fCode == "TL": return "Thundery Showers"
    if fCode == "WC": return "Windy, Cloudy"
    if fCode == "WD": return "Windy"
    if fCode == "WF": return "Windy, Fair"
    if fCode == "WR": return "Windy, Rain"
    if fCode == "WS": return "Windy, Show"

class LocationForecast:
    location ="UKNl"
    code=""
    desc = ""



def getLocalNowcast2Hour(nea_webservice_url,nea_webservice_location):

    lF =  LocationForecast()
    try:
        ws_req = Request(
            nea_webservice_url,
            headers={'User-Agent': 'Mozilla/5.0'})
        ws_response = urllib.request.urlopen(ws_req).read()

        logging.debug(ws_response)
        ws_root= etree.fromstring(ws_response)
        #locForecast = ws_root.findall("channel/item/weatherForecast/area[@name='"+location0 + "']/@forecast")
        #locForecast = ws_root.find("./channel/item/weatherForecast/area[@name='"+location0 + "']")
        locForecast = ws_root.find("./item/weatherForecast/area[@name='"+nea_webservice_location + "']")

        #print(locForecast)
        if locForecast is None:
            logging.error("Invalid Location/Schema Error " + nea_webservice_location )
            return lF

        #print(locForecast.attrib['forecast'])
        lF.code=locForecast.attrib['forecast']
        lF.location=nea_webservice_location
        lF.desc = mapNEAForcasteCode(locForecast.attrib['forecast'])

        #ws_doc = libxml2.parseDoc(ws_response)
        #ctxt = ws_doc.xpathNewContext()
        #res = ws_doc.xpathEval("/channel/item/weatherForecast/area[1]")
        #res = ws_doc.xpathEval("/channel/item/weatherForecast/area[@name='Jurong West']/@forecast")

        #res = ws_doc.xpathEval("/channel/item/weatherForecast/area[@name='"+location0 + "']/@forecast")
        #lF.code=res[0].content
        #lF.location=location0
        #lF.desc = mapNEAForcasteCode(res[0].content)
        #print(res.get("forecast"))
    except urllib.error.URLError as errMsg:
        logging.error("Connection Error "+ str(errMsg))
    except IndexError as iErrMsg:
        logging.error("Invalid Location/Schema Error " + nea_webservice_location +  str(iErrMsg))
    return lF

def neaWeatherDaemon():
    config = initConfig()
    nea_webservice_url = config.get('NEAWebService', 'nea_ws_url')
    nea_webservice_location = config.get('NEAWebService', 'nea_ws_location')
    nea_webservice_pollinterval_minutes = config.get('NEAWebService', 'nea_ws_poll_interval_minutes')
    logging.info(nea_webservice_url)
    while 1:
        locForcast= getLocalNowcast2Hour(nea_webservice_url,nea_webservice_location)
        logging.info("NEA LookupInfo :" +  locForcast.location  + " > " +  locForcast.code +"." + locForcast.desc)

        paramDataArray = {}
        paramDataArray['weather_code'] = locForcast.code
        paramDataArray['weather_desc'] = locForcast.desc
        paramDataArray['weather_location'] = locForcast.location
        webserviceInvokeAction(config,"neaweather", paramDataArray)

        #webserviceInvokeAction(locForcast.code)

        #    "nea_2hourforecast?weather_code=" + locForcast.code +
        #    "&weather_desc" + locForcast.desc +
        #    "&weather_location" + locForcast.location )
        #print(getLocalNowcast2Hour("Jurong West").desc)
        #print(getLocalNowcast2Hour("Pioneer").desc)
        #print(getLocalNowcast2Hour("Test Invalid").desc)
        logging.info("Sleep for Minutes: " + str(nea_webservice_pollinterval_minutes))
        time.sleep(int(nea_webservice_pollinterval_minutes) * 60)



if __name__ == '__main__':
    wDaemon = threading.Thread(name='daemon', target=neaWeatherDaemon)
    wDaemon.setDaemon(True)
    wDaemon.start()
    wDaemon.join()




