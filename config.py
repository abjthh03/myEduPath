import os
import mysql.connector

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.environ["DB_HOST"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            database=os.environ["DB_NAME"],
            port=int(os.environ["DB_PORT"])
        )
        return conn
    except Exception as e:
        print("❌ Database connection failed:", e)
        return None

