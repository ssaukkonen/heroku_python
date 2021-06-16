from flask import Flask
from flask import render_template
import psycopg2
from psycopg2 import Error
import textwrap
import os

app = Flask(__name__)
global averageT, averageH, maxT, minT, maxH, minH, lastT, lastH, lastTime

def databaseF():
    global averageT, averageH, maxT, minT, maxH, minH, lastT, lastH, lastTime
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        #print('url ', DATABASE_URL)

        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()

        postgres_insert_query = """SELECT AVG(CAST(temp AS FLOAT)), AVG(CAST(hum AS FLOAT)) FROM data"""
        cursor.execute(postgres_insert_query)
        temp = cursor.fetchone()
        averageT = str(round(temp[0],2))
        averageH = str(round(temp[1],2))
        print(averageT, averageH)
        
        postgres_insert_query = """SELECT MAX(CAST(temp AS FLOAT)), MIN(CAST(temp AS FLOAT)), MAX(CAST(hum AS FLOAT)), MIN(CAST(hum AS FLOAT)) FROM data"""
        cursor.execute(postgres_insert_query)
        temp = cursor.fetchone()
        maxT = str(temp[0])
        minT = str(temp[1])
        maxH = str(temp[2])
        minH = str(temp[3])        
        print(maxT, minT, maxH, minH)
        
        postgres_insert_query = """SELECT temp, hum, timedate FROM data order by id desc limit 1"""
        cursor.execute(postgres_insert_query)
        temp = cursor.fetchone()
        lastT = temp[0]
        lastH = temp[1]
        lastTime = temp[2]
        print(lastT, lastH, lastTime)        
        
    except (Exception, Error) as error:
        print(error)
    finally:
        if (connection):
            #return results
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    

@app.route("/")
@app.route('/index')
def index():
    global averageT, averageH, maxT, minT, maxH, minH, lastT, lastH, lastTime
    databaseF()
    return render_template('index.html', lastT=lastT, lastH=lastH, lastTime=lastTime,
                           averageT=averageT, averageH=averageH, maxT=maxT, minT=minT,
                           maxH=maxH, minH=minH)
    #return averageT
    #return "Hello World!"

