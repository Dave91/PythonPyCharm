from PyQt5.QtSql import QSqlQuery
import sqlite3


# query = "SELECT * FROM dict WHERE eng LIKE '" + ker + "%'"
# cur.execute('SELECT * FROM dict WHERE eng LIKE ?', (ker,))

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

ker = vmi
insertDataQuery.addBindValue(ker)
insertDataQuery.exec()
return
