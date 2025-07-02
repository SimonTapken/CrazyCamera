import sqlite3
import Klt
import KltTracked

class DatabaseFile:

    dbName = ''
    conn = sqlite3.connect('kltDB.db')
    cursor = conn.cursor()

    def __init__(self, dbName):
        self.dbName = dbName

    def creatTables(self):
        self.cursor.execute("""CREATE TABLE kltGeneral (
                                kltIdentification integer PRIMARY KEY NOT NULL, 
                                name text  NOT NULL,
                                menge real NOT NULL
                               )""")

        self.cursor.execute("""CREATE TABLE kltTracking (
                                trackingIdentification integer NOT NULL,
                                xPosition integer,
                                yPosition integer,
                                pointOfTime text NOT NULL
                                )""")

    def loadTablesTest(self):
        self.cursor.execute("INSERT INTO kltTracking VALUES (5, 4, 3, 12.34)")
        self.cursor.execute("INSERT INTO kltTracking VALUES (4, 3, 4, 1255.34)")
        self.cursor.execute("INSERT INTO kltGeneral VALUES (5, 'schrauben', 12.34)")
        self.cursor.execute("INSERT INTO kltTracking VALUES (4, 3, 7, 56)")
        self.cursor.execute("INSERT INTO kltGeneral VALUES (4, 'nägel', 7.56)")

    #cursor.execute("SELECT * FROM kltTracking WHERE xPosition='4'")
    #print(cursor.fetchone())
    #print(cursor.fetchmany(5))
    #print(cursor.fetchall())

    def insert_new_klt (self, klt):
        self.cursor.execute("INSERT INTO kltGeneral VALUES (:kltIdentification, :name, :menge)", {"kltIdentification": klt.id, "name": klt.name, "menge": klt.menge})
        self.conn.commit()

    def insert_new_klt_tracked(self, kltTracked):
        self.cursor.execute("INSERT INTO kltTracking VALUES (:trackingIdentification, :xPosition, :yPosition, :pointOfTime)", {"trackingIdentification": kltTracked.id, "xPosition": kltTracked.xPosition, "yPosition": kltTracked.yPosition, "pointOfTime": kltTracked.pointOfTime})
        self.conn.commit()

    def showall_kltGeneral(self):
        self.cursor.execute("SELECT * FROM kltGeneral")
        self.conn.commit()
        return self.cursor.fetchall()

    def showall_kltTracking(self):
        self.cursor.execute("SELECT * FROM kltTracking")
        self.conn.commit()
        return self.cursor.fetchall()

    def get_klt_by_id(self, ide):
        self.cursor.execute('''SELECT kltIdentification, name, menge, xPosition, yPosition, pointOfTime FROM kltGeneral INNER JOIN kltTracking ON kltGeneral.kltIdentification = kltTracking.trackingIdentification 
                       WHERE kltGeneral.kltIdentification=:identificationNumber''', {"identificationNumber": ide})
        self.conn.commit()
        return self.cursor.fetchall()

    def remove_klt(self, id):
        self.cursor.execute("DELETE from kltGeneral WHERE identificationNumber=:identificationNumber", {"identificationNumber": id})
        self.cursor.execute("DELETE from kltTracking WHERE identificationNumber=:identificationNumber", {"identificationNumber": id})
        self.conn.commit()

    def closeDatabase(self):
        self.conn.commit()
        self.conn.close()

