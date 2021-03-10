import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
# from PyQt5.QtWidgets import (QApplication as Qapp,
#                             QMessageBox as Qmsg,
#                             QLabel)
import csv


con = QSqlDatabase.addDatabase("QSQLITE")
con.setDatabaseName("dictvalami.db")
# db = Qsqldb.database("con", open=False)

# app = Qapp(sys.argv)

if not con.open():
    # Qmsg.critical(None, "Dictionary - Error!",
    #              "Database Error: %s" % con.lastError().databaseText(),)
    sys.exit(1)



'''dataquery = QSqlQuery()
dataquery.exec("SELECT eng, hun FROM dicts")'''


'''
insertDataQuery = QSqlQuery()
insertDataQuery.prepare(
    """
    INSERT INTO dicts (
        eng,
        hun
    )
    VALUES (?, ?)
    """
)

with open("dict_data/valami.csv", encoding="ansi") as csvfile:
    csvolv = csv.DictReader(csvfile, delimiter=";", fieldnames=("eng", "hun"))
    for row in csvolv:
        eng = row["eng"]
        hun = row["hun"]
        insertDataQuery.addBindValue(eng)
        insertDataQuery.addBindValue(hun)
        insertDataQuery.exec()
'''

'''
createTableQuery = QSqlQuery()
createTableQuery.exec(
    """
    CREATE TABLE dicts (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        eng VARCHAR(50) NOT NULL,
        hun VARCHAR(50) NOT NULL
    )
    """
)
'''

'''win = QLabel("Connection successfully opened!")
win.setWindowTitle("Dictionary")
win.resize(200, 100)
win.show()
sys.exit(app.exec_())'''
