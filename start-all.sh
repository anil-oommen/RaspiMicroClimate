#!/usr/bin/env bash

python3 mainFlaskWebApp.py &> logs/flask_webapp.sysout &
python3 mainListenArduinoSerialIReci.py &> logs/gpio_ir_arudino_reciever.sysout &
python3 mainNEAWeatherData.py &> logs/nea_weather_data.sysout &
python3 mainDHT22Collector.py &> logs/dbt22_sensor_collector.sysout &

echo "  ------ Waiting for processs to start"
sleep 5
echo "  ------ Listing running process"
ps -aef | grep python | grep -v "grep"
echo "  ------ Listing log files "
ls -l logs/*.sysout