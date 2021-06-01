import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='root',
            database='cc15'
        )
        self.csr = self.conn.cursor()

    def select(self, sqlStatement, sqlData = None):
        if sqlData == None:
            self.csr.execute(sqlStatement)
        else:
            self.csr.execute(sqlStatement, sqlData)
        return self.csr.fetchall()

    def save(self, sqlStatement, sqlData):
        self.csr.execute(sqlStatement, sqlData)
        self.conn.commit()

    def __del__(self):
        self.csr.close()
        self.conn.close()