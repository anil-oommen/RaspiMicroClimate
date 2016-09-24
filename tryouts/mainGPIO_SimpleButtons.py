
'''

The GPIO Interface Main Program.
Listen to Button press and invoke the webservice module
Connection : PIN 16 , PIN 6 (Ground) See Diagram


'''



from time import sleep
import time
import RPi.GPIO as GPIO

# Local Modules to include
from modWSCommon import webserviceInvokeAction
from modAppConfig import initConfig

GPIO.setmode(GPIO.BOARD)
PowerButton=16
GPIO.setup(PowerButton,GPIO.IN,pull_up_down=GPIO.PUD_UP)

last_action=0
ACTION_PRESS_ON = 9


press_start = time.time()

continue_to_listen=1

config = initConfig()


def shortPress():
    #print("Short Press")
    paramDataArray = {}
    paramDataArray['power'] = "short_press"
    webserviceInvokeAction(config, "gpio_input", paramDataArray)
def longPress():
    #print("Long Press")
    paramDataArray = {}
    paramDataArray['power'] = "long_press"
    webserviceInvokeAction(config, "gpio_input", paramDataArray)
def veryLongPress():
    #print("Very Long Press")
    paramDataArray = {}
    paramDataArray['power'] = "very_long_press"
    webserviceInvokeAction(config, "gpio_input", paramDataArray)

while(continue_to_listen):
    if GPIO.input(PowerButton)==0 and last_action==0:
        ##print ("Start Pressing")
        last_action= ACTION_PRESS_ON
        press_start = time.time()
    #elif GPIO.input(PowerButton)==0:
    #    print ("Waiting to release ")
    elif GPIO.input(PowerButton) != 0 and last_action  != 0:
        done = time.time()
        elapsed = done - press_start
        last_action=0
        #
        # print ("Hand Released Elapsed", elapsed )
        if elapsed <1 and elapsed > 0.2:
            shortPress()
        if elapsed > 1 and elapsed < 3:
            longPress()
        if elapsed >3:
            veryLongPress()
    sleep(.3)




