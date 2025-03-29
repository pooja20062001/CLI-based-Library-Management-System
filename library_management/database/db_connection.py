import sqlite3
from sqlite3 import Error
class DBConnection:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None
    def connect(self):
        # print("Connected Successfully")
        try:
            self.connection = sqlite3.connect(self.db_file)
           
            
            return self.connection 
        except sqlite3.Error as e:
            print(f"Database error:{e}") 
            
    def close(self):
        try: 
            if self.connection:
                self.connection.close()
                # print("Connection Closed")
        except sqlite3.Error as e:
            print(f"Database error:{e}")
        
            
db = DBConnection("library.db")  
db.connect()
db.close() 