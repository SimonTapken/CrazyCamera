from database.src.DatabaseFile import DatabaseFile

db = DatabaseFile('kltDB')
#db.creatTables()
#db.loadTablesTest()
#db.clear_GeneralTable()
#db.clear_TrackingTable()
print(db.get_klt_by_id(5))
print(db.get_klt_by_id(5))
print(db.get_klt_by_id(4))
print(db.showall_kltGeneral())
print(db.showall_kltTracking())
db.closeDatabase()