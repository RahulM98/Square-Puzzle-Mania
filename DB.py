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
        #print("In update")
        #self.show_table('beginner')
        self.c.execute("UPDATE {} SET played=?,moves=?,hints=?,time=?,score=? WHERE score=?;".format(t_name),(played,moves,hints,time,score,score))
        #self.show_table('beginner')
        self.conn.commit()

    def addition_deletion(self,t_name,played,moves,hints,time,score):
        #print("In addition")
        #self.show_table('beginner')
        self.c.execute("INSERT INTO {} (played,moves,hints,time,score) VALUES(?,?,?,?,?);".format(t_name),(played,moves,hints,time,score))
        #self.show_table('beginner')
        #self.c.execute("SELECT score FORM beginner ORDER BY score LIMIT 1")
        self.c.execute("SELECT COUNT(score) FROM {}".format(t_name))
        if list(self.c.fetchone())[0] > 3:
            self.c.execute("DELETE FROM {} WHERE (score,sl_no)=(SELECT score,sl_no FROM {} ORDER BY score LIMIT 1);".format(t_name,t_name))
        #self.show_table('beginner')
        self.conn.commit()

    def show_table(self,t_name):
        self.c.execute("SELECT score,moves,hints,time,played FROM {} ORDER BY score DESC;".format(t_name))
        res = self.c.fetchall()
        print("\n\n")
        for i in res:
            print(i)
        return res

    def get_scores(self,t_name):
        self.c.execute("SELECT score FROM {} ORDER BY score DESC;".format(t_name))
        res = self.c.fetchall()
        return res
    
#a = database()
#"""a.addition_deletion('beginner','2015-11-05 14:29:36',5,2,'14:29:36',54)
#a.addition_deletion('beginner','2015-11-05 14:29:36',1,4,'14:29:36',64)
#a.addition_deletion('beginner','2015-11-05 14:29:36',9,7,'14:29:36',60)
#a.show_table('beginner')"""
#a.update_table('beginner','2015-11-05 14:29:36',5,3,'14:29:36',54)
#a.update_table('beginner','2015-11-05 14:29:36',5,2,'14:29:36',64)
#a.update_table('beginner','2015-11-05 14:29:36',5,2,'14:29:36',60)
#a.show_table('beginner')
#a.c.close()
#a.conn.close()