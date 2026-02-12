import os
import mysql.connector


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get("MYSQLHOST"),
            user=os.environ.get("MYSQLUSER"),
            password=os.environ.get("MYSQLPASSWORD"),
            database=os.environ.get("MYSQLDATABASE"),
            port=int(os.environ.get("MYSQLPORT", 3306))
        )
        return connection

    except mysql.connector.Error as err:
        print("Database connection failed:", err)
        return None
