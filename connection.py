import os
import logging
from mysql.connector import connect, Error


def open_connection():
    return connect(
        host=os.getenv("KITBOY_DB_HOST", "localhost"),
        user=os.getenv("KITBOY_DB_USER", "root"),
        password=os.getenv("KITBOY_DB_PASSWORD", ""),
        database=os.getenv("KITBOY_DB_NAME", "kitboy"),
        connection_timeout=5,
    )


def dbcon(self):
    try:
        self.con = open_connection()
        self.cur = self.con.cursor()
    except Error:
        logging.exception("Could not connect to the Kitboy database")
        self.con = None
        self.cur = None