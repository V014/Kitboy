# database connection
import os
from mysql.connector import connect, Error

def dbcon(self):
    try:
        self.con = connect(
            host="localhost",
            user="root",
            passwd="",
            database="kitboy"
        )
        self.cur = self.con.cursor()
    except Error as e:
        print(f"Error connecting to database: {e}")
        self.con.rollback()
        self.con = None
        self.con.close()
        self.cur = None