class LibraryError(Exception):
    pass

class UserAlreadyExists(LibraryError):
    def __init__(self, message = 'User already exists'):
        self.message = message
        super().__init__(message)

class UserNotFound(LibraryError):
    def __init__(self, message = 'User not found'):
        self.message = message
        super().__init__(message)
        
class BookNotFound(LibraryError):
    def __init__(self, message = 'Book not found'):
        self.message = message
        super().__init__(message)
        
class DuplicateBookISBNError(LibraryError):
    def __init__(self, message = 'Book already exists' ):
        self.message = message
        super().__init__(message)

class TransactionNotFound(LibraryError):
    def __init__(self, message='Transaction not found'):
        self.message = message
        super().__init__(message)
        