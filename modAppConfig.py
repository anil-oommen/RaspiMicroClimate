import logging
import os
import configparser




def loadConfigFile(configObj, configFileName):
    if os.path.isfile(configFileName):
        configObj.read(configFileName)
        print("Config File Loaded:" , configFileName)
    else:
        print("Config File Not found:", configFileName)

def initConfig():
    config = configparser.ConfigParser(allow_no_value=True)
    loadConfigFile(config,"default.appconfig.ini")
    loadConfigFile(config,"../overide.appconfig.ini")
    loadConfigFile(config,"~/overide.appconfig.ini")
    return config


