import serial
import time

# Local Modules to include
from modAppConfig import initConfig
from modWSCommon import webserviceInvokeAction

ser = serial.Serial('/dev/ttyACM0', 9600)

config = initConfig()

prevTimeMillSecs = int(round(time.time() * 1000))
MAX_COMMAND_INTERVAL_MSECS = 500 # MilliSecs
strCommandLine1 = ""
def captureIRStream1Line(streamDataLine):
    global prevTimeMillSecs
    global strCommandLine1
    currTimeMillSecs  = int(round(time.time() * 1000))
    diffTimeMSecs = currTimeMillSecs - prevTimeMillSecs

    print ("+" + streamDataLine + " " + str(diffTimeMSecs)
           + "  " + strCommandLine1)

    # reset Prev line if more that interval
    if (diffTimeMSecs > MAX_COMMAND_INTERVAL_MSECS):
        strCommandLine1 = ""

    if (strCommandLine1 == "" and diffTimeMSecs > MAX_COMMAND_INTERVAL_MSECS ):
        # New Command Stream Line 1
        strCommandLine1 = streamDataLine
    elif (len(strCommandLine1)>0 and diffTimeMSecs <= MAX_COMMAND_INTERVAL_MSECS ):
        # Second Line read to Pass
        captureIRStreamFull(strCommandLine1,streamDataLine)
        strCommandLine1 = ""
    else :
        #Reset Everything
        strCommandLine1 = ""

    prevTimeMillSecs  = int(round(time.time() * 1000))

prevIRStreamFull = ""
def captureIRStreamFull(streamDataLine1, streamDataLine2):
    global prevIRStreamFull
    currIRStreamFull = streamDataLine1 + streamDataLine2
    interpetFullCommand(currIRStreamFull)
    #Debug of Changed Data
    if(prevIRStreamFull != ""):
        iChar = 0
        varMaskString = ""
        while iChar < len(currIRStreamFull) and iChar < len(prevIRStreamFull):
            diffChar = "_"
            if(currIRStreamFull[iChar] != prevIRStreamFull[iChar]):
                diffChar = currIRStreamFull[iChar]
            varMaskString  = varMaskString + diffChar
            iChar = iChar+1
        print(varMaskString)
    prevIRStreamFull = currIRStreamFull

def interpetFullCommand(theCommand):
    wx_command_power = "UKN"
    wx_command_temp = "UKN"
    wx_command_mode = "UKN"

    print(tagEmbedString)
    #re.sub(r'\W+', '', theCommand)
    #print(theCommand)

    #The ON OFF Mode
    if(theCommand[4-1]=="1"):
        wx_command_power=  "ON"
    elif (theCommand[4-1] == "0"):
        wx_command_power = "OFF"

    print(wx_command_power)

    #The Temperature settings
    if (theCommand[9-1:13-1] == "0000"):
        wx_command_temp =  "16.0"
    elif (theCommand[9-1:13-1] == "1000"):
        wx_command_temp =  "17.0"
    elif (theCommand[9-1:13-1] == "0100"):
        wx_command_temp =  "18.0"
    elif (theCommand[9-1:13-1] == "1100"):
        wx_command_temp =  "19.0"
    elif (theCommand[9-1:13-1] == "0010"):
        wx_command_temp =  "20.0"
    elif (theCommand[9-1:13-1] == "1010"):
        wx_command_temp =  "21.0"
    elif (theCommand[9-1:13-1] == "0110"):
        wx_command_temp =  "22.0"
    elif (theCommand[9-1:13-1] == "1110"):
        wx_command_temp =  "23.0"
    elif (theCommand[9-1:13-1] == "0001"):
        wx_command_temp =  "24.0"
    elif (theCommand[9-1:13-1] == "1001"):
        wx_command_temp =  "25.0"
    elif (theCommand[9-1:13-1] == "0101"):
        wx_command_temp =  "26.0"
    elif (theCommand[9-1:13-1] == "1101"):
        wx_command_temp =  "27.0"
    elif (theCommand[9-1:13-1] == "0011"):
        wx_command_temp =  "28.0"
    elif (theCommand[9-1:13-1] == "1011"):
        wx_command_temp =  "29.0"
    elif (theCommand[9-1:13-1] == "0111"):
        wx_command_temp =  "30.0"

    print(wx_command_temp)

    # The Modes settings
    if (theCommand[1-1:5-1] == "0001"):
        wx_command_mode =  "AUTO"
    elif (theCommand[1-1:5-1] == "1001"):
        wx_command_mode =  "COOL"
    elif (theCommand[1-1:5-1] == "0101"):
        wx_command_mode = "DRY"
    elif (theCommand[1-1:5-1] == "1101"):
        wx_command_mode = "FAN"
    elif (theCommand[1-1:5-1] == "0011"):
        wx_command_mode = "HEAT"

    print(wx_command_mode)

    paramDataArray = {}
    paramDataArray['power'] = wx_command_power
    paramDataArray['temp'] = wx_command_temp
    paramDataArray['mode'] = wx_command_mode
    webserviceInvokeAction(config, "aircon_ir_input", paramDataArray)

    return "NULL"

#print("b'IR/bin[11111111111111111111111111111111]\r\n"[2:])

while 1:
    serial_line = ser.readline()

    # Format recieved from Arudino
    # "b'IR/bin[11111111111111111111111111111111]\r\n"
    i=0
    tagEmbedDate= False
    tagEmbedString = ""
    tagContainValidData = False
    while i < len(serial_line):
        if (serial_line[i] == 91):
            tagEmbedDate = True
        elif (serial_line[i] == 93):
            tagEmbedDate = False
        elif (tagEmbedDate):
            tagEmbedString = tagEmbedString + chr(serial_line[i])
            if (chr(serial_line[i]) != '1'):
                tagContainValidData = True
        i += 1
    #print(tagEmbedString)
    #print(serial_line) # If using Python 2.x use: print serial_line
    #print(serial_line[2:]) # If using Python 2.x use: print serial_line
    # Do some other work on the data
    if (tagContainValidData) :
        captureIRStream1Line(tagEmbedString)

    time.sleep(0.05)

    # Loop restarts once the sleep is finished

ser.close() # Only executes once the loop exits