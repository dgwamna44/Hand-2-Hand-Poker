import sqlite3
from sqlite3 import Error
from tkinter import messagebox

def create_connection(db):
    try:
        conn = sqlite3.connect(db)
        return conn
    except Error as err:
        print(err)
    return None

def create_table(conn, database):
    sql_poker_table = """CREATE TABLE IF NOT EXISTS poker (
                            id integer PRIMARY KEY,
                            first_name text NOT NULL,
                            last_name text NOT NULL,
                            wins integer NOT NULL,
                            losses integer NOT NULL,
                            draws integer NOT NULL
                            ); """

    conn = create_connection(database)
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(sql_poker_table)
        except Error as e:
            print(e)
    else:
        messagebox.showerror("Error", "Couldn't connect to " + str(database))

def add_game(conn, first_name, last_name, wins, losses, draws):
    sql = """ INSERT INTO poker(first_name, last_name, wins, losses, draws) 
              VALUES(?,?,?,?,?)"""
    info = (first_name, last_name, wins, losses, draws)
    cur = conn.cursor()
    cur.execute(sql, info)