from flask import render_template, flash, redirect, request, Response ,send_from_directory, send_file
import json
from app import app
from modAppConfig import initConfig
from time import gmtime, strftime, localtime

import sqlite3
config = initConfig()

curr_nea_weather_code ='NA'
curr_nea_weather_desc ='NA'
curr_nea_weather_location ='NA'
curr_nea_weather_lastfeed = 'NA'


curr_dht22_temperature_dc='NA'
curr_dht22_humidity_pc='NA'
curr_dht22_lastfeed= 'NA'

curr_acir_power='NA'
curr_acir_temp='NA'
curr_acir_mode='NA'
curr_acir_lastfeed='NA'



# index view function suppressed for brevity



@app.route('/rmc_ws/neaweather', methods=['GET'])
def rmcWebServiceNEA():
    #Not using Forms, issues with Field Mappings
    weather_code = request.args.get('weather_code')
    weather_desc = request.args.get('weather_desc')
    weather_location = request.args.get('weather_location')
    if weather_code and weather_desc and weather_location :
        db = sqlite3.connect(config.get('AppDatabase', 'db_path'))
        cursor = db.cursor()
        records = [('NEA_CLIMATE', 'weather_code', weather_code),
                    ('NEA_CLIMATE', 'weather_desc', weather_desc),
                    ('NEA_CLIMATE', 'weather_location', weather_location)]
        cursor.executemany(
            ''' INSERT INTO rmc_feed_events(source, param_name, param_value,create_dt,create_time ) VALUES(?,?,?,date('now', 'localtime'),datetime('now', 'localtime'))''',
        records)

        global curr_nea_weather_code
        global curr_nea_weather_desc
        global curr_nea_weather_location
        global curr_nea_weather_lastfeed

        curr_nea_weather_code=weather_code
        curr_nea_weather_desc = weather_desc
        curr_nea_weather_location = weather_location
        curr_nea_weather_lastfeed = strftime("%b %d %H:%M", localtime())


        cursor.close()
        db.commit()
        return "SUCCESS"
    else:
        #print(weather_code + weather_desc+ weather_location)
        return "ERR:Missing Arguments"


@app.route('/rmc_ws/dht22sensor', methods=['GET'])
def rmcWebServiceDHT22():
    #Not using Forms, issues with Field Mappings
    temperature_dc = request.args.get('temperature_dc')
    humidity_pc = request.args.get('humidity_pc')
    if temperature_dc and humidity_pc :
        db = sqlite3.connect(config.get('AppDatabase', 'db_path'))
        cursor = db.cursor()
        records = [ ('DHT22_SENSOR', 'temperature_dc', temperature_dc),
                    ('DHT22_SENSOR', 'humidity_pc', humidity_pc)]
        cursor.executemany(
            ''' INSERT INTO rmc_feed_events(source, param_name, param_value,create_dt,create_time ) VALUES(?,?,?,date('now', 'localtime'),datetime('now', 'localtime'))''',
        records)
        global curr_dht22_temperature_dc
        global curr_dht22_humidity_pc
        global curr_dht22_lastfeed

        #curr_dht22_temperature_dc = print("{0:.1f}".format(float(temperature_dc)))
        #curr_dht22_humidity_pc = print("{0:.1f}".format(float(humidity_pc)))

        curr_dht22_temperature_dc = temperature_dc[:4]
        curr_dht22_humidity_pc = humidity_pc[:4]

        curr_dht22_lastfeed = strftime("%b %d %H:%M", gmtime())

        cursor.close()
        db.commit()
        return "SUCCESS"
    else:
        #print(weather_code + weather_desc+ weather_location)
        return "ERR:Missing Arguments"

@app.route('/rmc_ws/aircon_ir_input', methods=['GET'])
def rmcWebServiceAirconIR():
    #Not using Forms, issues with Field Mappings
    power = request.args.get('power')
    temp = request.args.get('temp')
    mode = request.args.get('mode')
    if power and temp and mode :
        db = sqlite3.connect(config.get('AppDatabase', 'db_path'))
        cursor = db.cursor()
        records = [ ('AIRCON_IR_INPUT', 'power_onoff', power),
                    ('AIRCON_IR_INPUT', 'temperature_dc', temp),
                    ('AIRCON_IR_INPUT', 'mode', mode)]
        cursor.executemany(
            ''' INSERT INTO rmc_feed_events(source, param_name, param_value,create_dt,create_time ) VALUES(?,?,?,date('now', 'localtime'),datetime('now', 'localtime'))''',
        records)
        global curr_acir_power
        global curr_acir_temp
        global curr_acir_mode
        global curr_acir_lastfeed

        curr_acir_power = power
        curr_acir_temp = temp
        curr_acir_mode = mode
        curr_acir_lastfeed = strftime("%b %d %H:%M", localtime())

        cursor.close()
        db.commit()
        return "SUCCESS"
    else:
        #print(weather_code + weather_desc+ weather_location)
        return "ERR:Missing Arguments"





@app.route('/rmc_ws/query', methods=['GET'])
def rmcWebServiceQueryFeed():
    #Not using Forms, issues with Field Mappings
    for_date = request.args.get('for_date')
    db = sqlite3.connect(config.get('AppDatabase', 'db_path'))
    cursor = db.cursor()
    cursor.execute('''
            SELECT id, source, param_name, param_value ,create_dt,create_time
            FROM rmc_feed_events order by id desc
            ''')
    all_rows = cursor.fetchall()
    feed_data = {
        "event": []
    }
    for row in all_rows:
        # row[0] returns the first column in the query (name), row[1] returns email column.
        #return row[0] + row[1] + row[2] + row[3] + row[4] + row[5]
        print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))
        feed_data['event'].append({
            "id": row[0],
            "source": row[1],
            "param_name": row[2],
            "param_value": row[3],
            "create_dt": row[4],
            "create_time": row[5],
        })

    cursor.close()
    db.commit()


    js = json.dumps(feed_data)

    resp = Response(js, status=200, mimetype='application/json')
    return resp



@app.route('/rmc_ws/now', methods=['GET'])
def rmcWebServiceNow():
    global curr_nea_weather_code
    global curr_nea_weather_lastfeed
    global curr_nea_weather_desc
    global curr_nea_weather_location

    global curr_dht22_temperature_dc
    global curr_dht22_humidity_pc
    global curr_dht22_lastfeed

    global curr_acir_power
    global curr_acir_temp
    global curr_acir_mode
    global curr_acir_lastfeed
    now_data = {
        "now": []
    }
    now_data['now'].append({
        'nea_weather_code': curr_nea_weather_code,
        'nea_weather_desc' : curr_nea_weather_desc,
        'nea_weather_location' : curr_nea_weather_location,
        'nea_weather_lastfeed': curr_nea_weather_lastfeed,

        'dht22_temperature_dc' :curr_dht22_temperature_dc,
        'dht22_humidity_pc' : curr_dht22_humidity_pc,
        'dht22_lastfeed' : curr_dht22_lastfeed,

        'acir_power': curr_acir_power,
        'acir_temp' : curr_acir_temp,
        'acir_mode' : curr_acir_mode,
        'acir_lastfeed' : curr_acir_lastfeed

    })
    js = json.dumps(now_data)

    resp = Response(js, status=200, mimetype='application/json')
    return resp





# Static Section

@app.route('/static/<path:path>')
def rmc_static(path):
    return send_from_directory('static', path)

@app.route('/node_modules/<path:path>')
def rmc_node_modules(path):
    return send_from_directory('node_modules', path)

@app.route('/rmc_ws/debug_ir_gpio')
def rmc_debug_ir_gpio():
    print("Delivering default File:gpio_ir_reciever.sysout")
    return send_file('../gpio_ir_reciever.sysout')


@app.route('/')
def rmc_default():
    print("Delivering default File:index.html")
    return send_file('index.html')

