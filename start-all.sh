#!/usr/bin/env bash

python3 mainFlaskWebApp.py > logs/flask_webapp.sysout 2>&1 &
#OLD Direct GPIO mainGPIOIRReci_FullRawState.py
#python3 mainGPIOIRReci_FullRawState.py > logs/gpio_ir_reciever.sysout 2>&1 &
python3 mainListenArduinoSerialIReci.py > logs/gpio_ir_arudino_reciever.sysout 2>&1 &
python3 mainNEAWeatherData.py > logs/nea_weather_data.sysout 2>&1 &
python3 mainDHT22Collector.py > logs/dbt22_sensor_collector.sysout 2>&1 &
sleep 5

ls -l logs/*.sysout