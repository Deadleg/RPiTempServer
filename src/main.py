from flask import Flask, render_template    
from datetime import datetime, timedelta
import pymysql
import pymysql.cursors

app = Flask(__name__)

weeklyInterval = 60
dailyInterval = 15

def getTemps(start = (datetime.now() - timedelta(days=7)), end = datetime.now(), interval = weeklyInterval):
    startString = "\'" + start.strftime("%Y-%m-%d %H:%M:%S") + "\'"
    endString = "\'" + end.strftime("%Y-%m-%d %H:%M:%S") + "\'"

    data = []
    connection = pymysql.connect(host='localhost', user='web', passwd='', db='thermometer', cursorclass=pymysql.cursors.DictCursor)    
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM (SELECT @row := @row + 1 AS rownum, reading_time, celsius_reading FROM (SELECT @row := 0) r, temperature_readings) RANKED WHERE (rownum % " + str(interval) + " = 1) AND (reading_time BETWEEN " + startString + " AND " + endString + ");"
            cursor.execute(sql)
            data = cursor.fetchall()
    finally:
        connection.close()

    return data

@app.route("/")
def weekly_temp():
    data = getTemps()
    current_temp = data[-1:][0][u'reading_time'].strftime('%m-%d %H:%M') + " : " + str(data[-1:][0][u'celsius_reading']/1000.)
    data = [(x[u'reading_time'], x[u'celsius_reading']/1000.) for i, x in enumerate(data)]

    templateData = {
            'title': 'temperature',
            'temp': current_temp,
            'data': data,
            'weekly' : True
        }
    return render_template('main.html', **templateData)

@app.route("/temp/daily")
def daily_temp():
    data = getTemps(start = (datetime.now() - timedelta(days=1)), interval = dailyInterval)
    current_temp = data[-1:][0][u'reading_time'].strftime('%m-%d %H:%M') + " : " + str(data[-1:][0][u'celsius_reading']/1000.)
    data = [(x[u'reading_time'], x[u'celsius_reading']/1000.) for i, x in enumerate(data)]

    templateData = {
            'title': 'temperature',
            'temp': current_temp,
            'data': data,
            'weekly' : False
        }
    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
