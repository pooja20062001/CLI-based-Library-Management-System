from library_management.models.transaction_model import Transactions
from library_management.database.transaction_queries import TransactionQueries
from library_management.utils import exceptions
from datetime import datetime

class TransactionServices:
    def __init__(self, db_file):
        self.db_file = db_file
        self.transaction_queries = TransactionQueries(self.db_file)
    def get_transaction_by_id(self, transaction_id):
        Transaction = self.transaction_queries.get_transaction_by_id(transaction_id=transaction_id)
        if Transaction:
            return Transaction
        else:
            raise exceptions.TransactionNotFound
    def get_transaction_by_user_id(self, user_id):
        Transaction = self.transaction_queries.get_transaction_by_user_id(user_id=user_id)
        if Transaction:
            return Transaction
    
    def borrow_book(self, user_id, book_id):
        borrowed_transaction = Transactions(user_id=user_id,book_id=book_id,borrowed_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                         
        transaction_id = self.transaction_queries.borrow_book(user_id=borrowed_transaction.user_id, book_id=borrowed_transaction.book_id,borrowed_date=borrowed_transaction.borrowed_date)
           
        if transaction_id:
            return transaction_id


    

    def return_book(self, transaction_id):
        return_transaction = self.transaction_queries.return_book(
        transaction_id=transaction_id, returned_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S %p"))
        
        if return_transaction:
            return return_transaction

    def is_returned(self, transaction_id):
        Transactions = self.get_transaction_by_id(transaction_id=transaction_id)
        if Transactions[4]:
         return True       

    def close_connection(self):
        self.transaction_queries.close_connection()