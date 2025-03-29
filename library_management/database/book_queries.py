import sqlite3
from library_management.database.db_connection import DBConnection
class BookQueries:
    def __init__(self,db_file):
        self.db_file=db_file
        self.db=DBConnection(self.db_file)
        self.connection=self.db.connect()
        self.cursor=self.connection.cursor()
        self.create_table()

    def  create_table(self):
        create_table_query="""
        CREATE TABLE IF NOT EXISTS book(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        isbn TEXT UNIQUE NOT NULL,
        avaliable_copies INTEGER  NOT NULL 
        );
        """ 
        self.cursor.execute(create_table_query) 
        self.connection.commit() 
        print('Book Table Created')

    def add_book(self,title,author,isbn,available_copies):
        try:
            add_book_query="""
            INSERT INTO book(title,author,isbn,avaliable_copies) VALUES(?,?,?,?);      
            """ 
            self.cursor.execute(add_book_query,(title,author,isbn,available_copies))  
            self.connection.commit()
            book_id=self.cursor.lastrowid
            print(f"Book wit ID:{book_id}added.")
            return book_id
        except sqlite3.Error as e:
            print(f'Database Error:{e}')
       
    def update_book(self,book_id,title=None,author=None,isbn=None,available_copies=None):
        update_fields=[]
        values=[]
        if title:
            update_fields.append("title=?")
            values.append(title)
        if author:
            update_fields.append("author=?")
            values.append(author)     
        if  isbn:  
            update_fields.append("isbn=?")
            values.append(isbn)
        if available_copies:
            update_fields.append("available_copies=?")
            values.append(available_copies)
        if not update_fields:
            print('You fool you have not provided any fields to update') 
            return 
        update_query=f"UPDATE books set{(', '.join(update_fields))} WHERE id = ?;"   
        values.append(book_id)  
        try:
            self.cursor.execute(update_query,tuple(values))
            self.connection.commit()
            print('Book update!!!')
        except sqlite3.Error as e:
            print(f'Database Error:{e}') 

    def get_book(self,book_id):
        try:
            select_query="""
            SELECT * FROM book WHERE id = ?;
            """ 
            self.cursor.execute(select_query,(book_id,))  
            book = self.cursor.fetchone()     
            # print(book)  
            return book
        except sqlite3.Error as e:
            print(f'Database Error: {e}')

    def get_all_book(self):
        try:
            select_query="""
            SELECT * FROM book;
            """ 
            self.cursor.execute(select_query)  
            book=self.cursor.fetchall()   
            print(book) 
            return book
        except sqlite3.Error as e:
            print(f'Database Error: {e}') 

    def remove_book(self,book_id):
        try:
            remove_query ="""
            DELETE FROM book WHERE id = ?;
            """  
            self.cursor.execute(remove_query,(book_id,)) 
            self.connection.commit()  
            print(f'Book with ID: {book_id}removed.')  
            return book_id
        except sqlite3.Error as e:
            print(f'Database Error: {e}')

    def close_connection(self):
        self.db.close()   

        
book_queries=BookQueries("library.db")     
# book_queries.add_book('Django the life','Pooja','12325835467',3) 
# book_queries.add_book('python the great','Tina','456763549125',12) 
# book_queries.add_book('Roadmap','Chinnu','735483967545',12)
# book_queries.get_book(3) 
# print('--------------') 
# book_queries.remove_book(3) 
# print('--------------') 
# book_queries.get_book(3)  
# book_queries.update_book(1,available_copies=11,author='Aishwarya')
# book_queries.update_book(1)
# book_queries.get_all_book()
book_queries.close_connection()