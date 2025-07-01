import sqlite3
import Klt
import KltTracked

conn = sqlite3.connect('kltDB.db')

cursor = conn.cursor()

#cursor.execute("""CREATE TABLE kltGeneral (
#                  kltIdentification integer PRIMARY KEY NOT NULL,
#                  name text  NOT NULL,
#                  menge real NOT NULL
#                  )""")

#cursor.execute("""CREATE TABLE kltTracking (
#                  trackingIdentification integer NOT NULL,
#                  xPosition integer,
#                  yPosition integer,
#                  pointOfTime text NOT NULL
 #                 )""")

#cursor.execute("INSERT INTO kltTracking VALUES (5, 4, 3, 12.34)")
#cursor.execute("INSERT INTO kltTracking VALUES (4, 3, 4, 1255.34)")
#cursor.execute("INSERT INTO kltGeneral VALUES (5, 'schrauben', 12.34)")
#cursor.execute("INSERT INTO kltTracking VALUES (4, 3, 7, 56)")
#cursor.execute("INSERT INTO kltGeneral VALUES (4, 'nägel', 7.56)")

#cursor.execute("SELECT * FROM kltTracking WHERE xPosition='4'")
#print(cursor.fetchone())
#print(cursor.fetchmany(5))
#print(cursor.fetchall())

def insert_new_klt (klt):
    cursor.execute("INSERT INTO kltGeneral VALUES (:kltIdentification, :name, :menge)", {"kltIdentification": klt.id, "name": klt.name, "menge": klt.menge})

def insert_new_klt_tracked(kltTracked):
    cursor.execute("INSERT INTO kltTracking VALUES (:trackingIdentification, :xPosition, :yPosition, :pointOfTime)", {"trackingIdentification": kltTracked.id, "xPosition": kltTracked.xPosition, "yPosition": kltTracked.yPosition, "pointOfTime": kltTracked.pointOfTime})

def showall_kltGeneral():
    cursor.execute("SELECT * FROM kltGeneral")
    return cursor.fetchall()

def showall_kltTracking():
    cursor.execute("SELECT * FROM kltTracking")
    return cursor.fetchall()

def get_klt_by_id(id):
    cursor.execute('''SELECT kltIdentification, name, menge, xPosition, yPosition, pointOfTime FROM kltGeneral INNER JOIN kltTracking ON kltGeneral.kltIdentification = kltTracking.trackingIdentification 
                   WHERE kltGeneral.kltIdentification=:identificationNumber''', {"identificationNumber": id})
    return cursor.fetchall()

def remove_klt(id):
    cursor.execute("DELETE from kltGeneral WHERE identificationNumber=:identificationNumber", {"identificationNumber": id})
    cursor.execute("DELETE from kltTracking WHERE identificationNumber=:identificationNumber", {"identificationNumber": id})

print(get_klt_by_id(5))
print(get_klt_by_id(4))
print(showall_kltGeneral())
print(showall_kltTracking())
conn.commit()

conn.close()