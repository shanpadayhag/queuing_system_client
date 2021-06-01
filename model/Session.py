import sqlite3, os

class Session:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(os.getcwd(), 'model/model.db'))
        self.csr = self.conn.cursor()
    
    def currentUser(self):
        self.csr.execute('SELECT * FROM session')
        return self.csr.fetchall()
    
    def updateCurrentUser(self, id):
        self.csr.execute('INSERT INTO session (`id`) VALUES (?);', (id,))
        self.conn.commit()
    
    def clearCurrentUser(self):
        self.csr.execute('DELETE FROM session')
        self.conn.commit()

    def __del__(self):
        self.csr.close()
        self.conn.close()

# Session().updateCurrentUser(1)
# Session().clearCurrentUser()
# print(Session().currentUser()[0][0])