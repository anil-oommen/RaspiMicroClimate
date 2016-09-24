sudo apt-get install sqlite3

rmc_store.db
rmc_initilize.sql
	CREATE TABLE rmc_feed_events(id INTEGER PRIMARY KEY,source TEXT, param_name TEXT,param_value TEXT,create_dt TEXT , create_time  TEXT );
rmc_destroy.sql
	DROP TABLE rmc_feed_events;



import sqlite3
db = sqlite3.connect('test_mydb')
cursor = db.cursor()
cursor.execute('''

''')

 SELECT date('now');
2016-09-23
sqlite> select datetime('now');


id = 100
source = 'NEA_CLIMATE'
param_name = 'local_weather'
param_value = 'HD'
cursor.execute('''INSERT INTO feed_events(id, source, param_name, param_value)
                  VALUES(?,?,?,?)''', (id,source, param_name, param_value))
print('First Record Inserted')


cursor.execute('''SELECT id, source, param_name, param_value  FROM feed_events order by id desc''')
all_rows = cursor.fetchall()
for row in all_rows:
    # row[0] returns the first column in the query (name), row[1] returns email column.
    print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))


records = [	('NEA_CLIMATE', 'local_weather', 'HD'),
			('NEA_CLIMATE', 'local_weather', 'HD'),
			('NEA_CLIMATE', 'local_weather', 'HD')]
cursor.executemany(''' INSERT INTO feed_events(source, param_name, param_value,create_dt,create_time ) VALUES(?,?,?,date('now'),datetime('now'))''', records)
db.commit()

db.commit()

db.close()




http://www.rototron.info/dht22-tutorial-for-raspberry-pi/

sudo apt-get install git
cd ~
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo apt-get update
sudo apt-get install build-essential python-dev
sudo python setup.py install

sudo python3 setup.py install

import sys
import Adafruit_DHT
humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 23)
if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)


