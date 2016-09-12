'''

Credits : Orignal Idea  for reading time sliced DataStream
https://blog.bschwind.com/2016/05/29/sending-infrared-commands-from-a-raspberry-pi-without-lirc/

Code has been built for Europace AC Remote YAG1FB ,
2 Frames Sent , Merge and Process , all unknows to be printed not passed to the webservice Calls.
Pulse Duration and Frame is just for this Remote.

'''

import RPi.GPIO as GPIO
import math
import os
from datetime import datetime
from time import sleep


# Local Modules to include
from modAppConfig import initConfig
from modWSCommon import webserviceInvokeAction


# This is for revision 1 of the Raspberry Pi, Model B
# This pin is also referred to as GPIO23
INPUT_WIRE = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(INPUT_WIRE, GPIO.IN)

config = initConfig()

def isSafeO(duration):
    if duration > 180 and duration < 790:
        return 1
    else:
        return 0

def isSafe1(duration):
    if duration > 450 and duration < 600:
        return 1
    else:
        return 0

def charRepresent0(duration):
    if isSafeO(duration):
        return " "
    elif duration > 7600 and duration < 9100:
        return "#"
    else:
        return "?"

def charRepresent1(duration):
    if isSafe1(duration):
        return " "
    elif duration > 400 and duration < 480:
        return "A"
    elif duration > 1550 and duration < 1650:
        return "A"
    elif duration > 4380 and duration < 4480:
        return "B"
    elif duration > 19800 and duration < 20300:
        return "C"
    elif duration > 39800 and duration < 40070:
        return "D"
    else:
        return "?"

hold_command_time= datetime.now()
hold_command_line1 = ""


def interpetCommand(theCommand):
    theCommandInterpret =""
    if(len(theCommand) < 120): # i dont understand this, and yes has to be 2 Framse, note its string length not mils
        return ".NOT_UNDERSTOOD.Len" + str(len(theCommand))

    wx_command_power = ".UKNo."
    wx_command_temp = ".UKNc."
    wx_command_mode = ".UKNm."

    #The ON OFF Mode
    if(theCommand[4]=="A"):
        wx_command_power=  ".ONN."
    elif (theCommand[4] == " "):
        wx_command_power = ".OFF."


    #The Temperature settings
    if (theCommand[9:13] == "    "):
        wx_command_temp =  ".16c."
    elif (theCommand[9:13] == "A   "):
        wx_command_temp =  ".17c."
    elif (theCommand[9:13] == " A  "):
        wx_command_temp =  ".18c."
    elif (theCommand[9:13] == "AA  "):
        wx_command_temp =  ".19c."
    elif (theCommand[9:13] == "  A "):
        wx_command_temp =  ".20c."
    elif (theCommand[9:13] == "A A "):
        wx_command_temp =  ".21c."
    elif (theCommand[9:13] == " AA "):
        wx_command_temp =  ".22c."
    elif (theCommand[9:13] == "AAA "):
        wx_command_temp =  ".23c."
    elif (theCommand[9:13] == "   A"):
        wx_command_temp =  ".24c."
    elif (theCommand[9:13] == "A  A"):
        wx_command_temp =  ".25c."
    elif (theCommand[9:13] == " A A"):
        wx_command_temp =  ".26c."
    elif (theCommand[9:13] == "AA A"):
        wx_command_temp =  ".27c."
    elif (theCommand[9:13] == "  AA"):
        wx_command_temp =  ".28c."
    elif (theCommand[9:13] == "A AA"):
        wx_command_temp =  ".29c."
    elif (theCommand[9:13] == " AAA"):
        wx_command_temp =  ".30c."



    # The Modes settings
    if (theCommand[1:5] == "   A"):
        wx_command_mode =  ".AUTO."
    elif (theCommand[1:5] == "A  A"):
        wx_command_mode =  ".COOL"
    elif (theCommand[1:5] == " A A"):
        wx_command_mode = ".DRY_."
    elif (theCommand[1:5] == "AA A"):
        wx_command_mode = ".FAN_."
    elif (theCommand[1:5] == "  AA"):
        wx_command_mode = ".HEAT."



    # The FAN Speed Settings
    # TODO but Differs from Mode to Mode, expected watch space 127 to end but chances of MisAlignment.


    theCommandInterpret = theCommandInterpret + wx_command_power + wx_command_temp + wx_command_mode


    paramDataArray = {}
    paramDataArray['power'] = wx_command_power
    paramDataArray['temp'] = wx_command_temp
    paramDataArray['mode'] = wx_command_mode
    webserviceInvokeAction(config, "aircon_ir_input", paramDataArray)

    return theCommandInterpret

while True:
    value = 1
    # Loop until we read a 0
    while value:
        value = GPIO.input(INPUT_WIRE)

    # Grab the start time of the command
    startTime = datetime.now()

    # Used to buffer the command pulses
    command = []

    # The end of the "command" happens when we read more than
    # a certain number of 1s (1 is off for my IR receiver)
    numOnes = 0

    # Used to keep track of transitions from 1 to 0
    previousVal = 0

    while True:

        if value != previousVal:
            # The value has changed, so calculate the length of this run
            now = datetime.now()
            pulseLength = now - startTime
            startTime = now

            command.append((previousVal, pulseLength.microseconds))

        if value:
            numOnes = numOnes + 1
        else:
            numOnes = 0

        # 10000 is arbitrary, adjust as necessary

        if numOnes > 10000:
            break

        previousVal = value
        value = GPIO.input(INPUT_WIRE)

    command_string = " ["
    # print "----------Start----------"
    for (val, pulse) in command:
        command_string = command_string + str(val) + ":" + hex(int(math.ceil(pulse / 100))) + " ";

    str_off_signature = ""
    str_onn_signature = ""

    for i in range(len(command)):
        if command[i][0] == 0 and charRepresent0(command[i][1]) =="?":
            print ("Report,Anomaly ON_0_OFF {0} {1} \t\t".format(i,command[i][1]))
        elif command[i][0] == 1 and charRepresent1(command[i][1]) =="?":
            print ("Report,Anomaly ON_1_ON  {0} {1} \t\t".format(i, command[i][1]))

        if command[i][0] == 0:
            str_off_signature = str_off_signature + charRepresent0(command[i][1])
        if command[i][0] == 1:
            str_onn_signature = str_onn_signature  + charRepresent1(command[i][1])
    str_off_signature = str_off_signature + ""
    str_onn_signature = str_onn_signature + ""



    #Frames can come 1 at a time or 2 at a time.
    #Each Frame will have 9 in the begin.
    #print(len(command))
    #print(str_off_signature)
    #print(str_onn_signature)


    hold_time = datetime.now()-hold_command_time


    if (len(command) > 137  and len(command) < 141) : # this is only One FRAME, Actual Size is 139
        #print(len(command), hold_time.microseconds/1000 )
        if hold_command_line1 !="" and hold_time.microseconds/1000 < 1000: # this is second Frame, came within shortTime, print both now
            print (hold_command_line1 + str_onn_signature + "\t\t*1+2_FRAMEJOIN  ", interpetCommand(hold_command_line1 + str_onn_signature ))
            # For Debug , ,HELD_FOR_MILSECS: hold_time.microseconds/1000,
            # hold_command_time = Leave this as is will expire
            hold_command_line1 = ""
        else:
            if hold_command_line1 != "":  # There was an old one that is expired now, purge it
                print (hold_command_line1 + "\t\t*1_FRAME_EXPIR  ",
                       interpetCommand(hold_command_line1 ))
                #For Debug , hold_time.microseconds / 1000,
                hold_command_line1 = ""

            hold_command_time = datetime.now()
            hold_command_line1 = str_onn_signature
    else:
        # This is an 2 FRAME Command , or an Unknown
        print (str_onn_signature +"\t\t*MULTI_FRAME" , len(command) , interpetCommand(str_onn_signature ))
        hold_command_line1 = ""





    #print ("Size of array is " + str(len(command)) + command_string + "] ")
