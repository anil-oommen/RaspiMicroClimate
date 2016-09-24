
python3 mainFlaskWebApp.py > flask_webapp.sysout 2>&1 &
python3 mainGPIOIRReci_FullRawState.py > gpio_ir_reciever.sysout 2>&1 &
python3 mainNEAWeatherData.py > nea_weather_data.sysout 2>&1 &
python3 mainDHT22Collector.py > dbt22_sensor_collector.sysout 2>&1 &
sleep 5

ls -l *.sysout