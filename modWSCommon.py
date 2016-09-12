# for Python 3
import urllib.request


def webserviceInvokeAction(config,webAction,paramDataArray):

    url_values = urllib.parse.urlencode(paramDataArray)

    ws_hostname = config.get('AppWSConnector', 'hostname')
    ws_port = config.get('AppWSConnector', 'host_port')
    webservice_invoke = "http://" + ws_hostname + ":"  + str(ws_port) +  "/action/" \
                        + webAction +"?" + url_values
    print ("Invoke WebServices:", webservice_invoke)
    ws_response =  ""
    try:
        ws_response = urllib.request.urlopen(webservice_invoke).read()
    except urllib.error.URLError as errMsg:
        print("Connection Error ", errMsg)
    else:
        print ("WebServices Response:", ws_response)


#Only for Testing Purpose
'''
if __name__ == '__main__':
    paramDataArray = {}
    paramDataArray['A']= 'B'
    paramDataArray['C']= 'D& '
    webserviceInvokeAction("TEST",paramDataArray)
'''