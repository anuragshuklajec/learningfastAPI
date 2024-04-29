import psycopg2
from psycopg2.extras import RealDictCursor
import time

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='root',cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("db connection succesfull")
        break
    except Exception as e:
        print("connection to database failed")
        print("Error : ", e)
        time.sleep(2)