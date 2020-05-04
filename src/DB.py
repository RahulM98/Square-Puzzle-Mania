## Title: DB.py
## Name : 
## @author : Rahul Manna
## Created on : 2020-04-26 16:53:10
## Description : 

import sqlite3 as lite

class database():
    def __init__(self):
        #connect database
        try:
            self.conn = lite.connect("file:puzzle.db?mode=rw",uri=True)
            self.c = self.conn.cursor()
        except:
            self.conn = lite.connect("puzzle.db")
            self.c = self.conn.cursor()
            levels = ['beginner','easy','medium','hard']
            for lvl in levels:
                self.c.execute("CREATE TABLE {}(sl_no INTEGER PRIMARY KEY,played DATETIME,hints INTEGER,moves INTEGER,time TIME,score INTEGER);".format(lvl))
                self.c.execute("INSERT INTO {}(score) VALUES(0.0)".format(lvl))
                self.c.execute("INSERT INTO {}(score) VALUES(0.0)".format(lvl))
                self.c.execute("INSERT INTO {}(score) VALUES(0.0)".format(lvl))
                self.conn.commit()

    def update_table(self,t_name,played,moves,hints,time,score):
        self.c.execute("UPDATE {} SET played=?,moves=?,hints=?,time=?,score=? WHERE score=?;".format(t_name),(played,moves,hints,time,score,score))
        self.conn.commit()

    def addition_deletion(self,t_name,played,moves,hints,time,score):
        self.c.execute("INSERT INTO {} (played,moves,hints,time,score) VALUES(?,?,?,?,?);".format(t_name),(played,moves,hints,time,score))
        self.c.execute("SELECT COUNT(score) FROM {}".format(t_name))
        if list(self.c.fetchone())[0] > 3:
            self.c.execute("DELETE FROM {} WHERE (score,sl_no)=(SELECT score,sl_no FROM {} ORDER BY score LIMIT 1);".format(t_name,t_name))
        self.conn.commit()

    def show_table(self,t_name):
        self.c.execute("SELECT score,moves,hints,time,played FROM {} ORDER BY score DESC;".format(t_name))
        res = self.c.fetchall()
        return res

    def get_scores(self,t_name):
        self.c.execute("SELECT score FROM {} ORDER BY score DESC;".format(t_name))
        res = self.c.fetchall()
        return res