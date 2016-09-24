from flask import render_template, flash, redirect, request, Response
import json
from app import app
from .forms import LoginForm
from modAppConfig import initConfig

import sqlite3
config = initConfig()





# index view function suppressed for brevity


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print(form.openid.data)
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/login')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


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
            ''' INSERT INTO rmc_feed_events(source, param_name, param_value,create_dt,create_time ) VALUES(?,?,?,date('now'),datetime('now'))''',
        records)
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
            ''' INSERT INTO rmc_feed_events(source, param_name, param_value,create_dt,create_time ) VALUES(?,?,?,date('now'),datetime('now'))''',
        records)
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
            ''' INSERT INTO rmc_feed_events(source, param_name, param_value,create_dt,create_time ) VALUES(?,?,?,date('now'),datetime('now'))''',
        records)
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
