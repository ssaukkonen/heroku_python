from flask import Flask
import psycopg2
from psycopg2 import Error
import textwrap
import os

app = Flask(__name__)

def databaseF():
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        print('url ', DATABASE_URL)

        connection = psycopg2.connect(DATABASE_URL, sslmode='require')

        cursor = connection.cursor()
        postgres_insert_query = """SELECT * from data"""
        #record_to_insert = (temp,humi,date)
        cursor.execute(postgres_insert_query)
        #connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into table")

    except (Exception, Error) as error:
        print(error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    

@app.route("/")
def index():
    return "Hello World!"

databaseF()
