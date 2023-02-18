import sqlite3 as sql
import os

class Db_Connection():
    def __init__(self):
        self.conn= None
    def check_database_exits(self,name):
        for file in os.listdir(os.getcwd()):
            if file ==name:
                return True
            else:
                return False
            break
    def build_connection(self,name):
        if self.check_database_exits(name)==True:
            print("Database already exist")
            self.conn = sql.connect(name)
        else:
            self.conn = sql.connect(name)
            print("Built new database.")
            print("connected")
        return self.conn
    def create_table(self):
        self.cursor = self.conn.cursor()
        try:
            print("Creating table....")
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS ARTICLES(Title text, Keyword text , Abstract text, Year text, Class_Name text)""")
            self.conn.commit()
            print("Created.")
        except Exception as e:
            print("created table error "+ e)
        return self.cursor
    def add_article(self,title,keyword,abstract,year,class_name):
        add_command = """INSERT INTO ARTICLES VALUES {}"""
        try:
            self.cursor.execute(add_command.format((title,keyword,abstract,year,class_name)))
            self.conn.commit()
        except Exception as e:
            print("add table error ")
            print(e)






