import os
import mysql.connector

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get("MYSQLHOST", "localhost"),
            user=os.environ.get("MYSQLUSER", "root"),
            password=os.environ.get("MYSQLPASSWORD", "root123"),
            database=os.environ.get("MYSQLDATABASE", "myedupath"),
            port=int(os.environ.get("MYSQLPORT", 3306))
        )
        return connection
    except mysql.connector.Error as err:
        print("Database connection failed:", err)
        return None
