from library_management.services.user_service import UserServices
from library_management.services.book_service import BookServices
from library_management.services.transaction_service import TransactionServices
from library_management.utils import exceptions
from library_management.animation import loader, dot_loader

# Can be utilized while registering the librarian
ADMIN_PASS = "libraryAdmin@123"

# Database file name
DB_NAME = 'library.db'
def establish_connection():
    global user_services, book_services, transaction_services
    user_services = UserServices(DB_NAME)
    book_services = BookServices(DB_NAME)
    transaction_services = TransactionServices(DB_NAME)

def break_connection():
    user_services.close_connection()
    book_services.close_connection()
    transaction_services.close_connection()


def main_menu():
    print("1. Register User")
    print("2. Manage Book (Librarian Only)")
    print("3. Borrow Book (Student Only)")
    print("4. Return Book")
    print("5. View All Book")
    print("6. View Transaction Detail By ID")
    print("7. View Transaction Detail By User ID")
    print("8. Exit")
    choice = input("Please Select an Option: ")
    return choice


# def main():
#     print("--Welcome to the Library Hub---")
#     print("Establishing connection")
#     establish_connection()
#     while True:
#         choice = main_menu()
#         if choice == "1":
#             print()
#         elif choice == "8":
#             print("Closing connection")
#             break_connection()
#             print("Thank You!, Visit Again!")
#             break
# if __name__ == "__main__":
#     main()


def user_registration():
    print('\n1.Librarian(Only Admin)')
    print('2.Student')
    user_type = input('Choose your user type:')
    try:
        if user_type == "1":
            admin_pass = input("Enter Admin Password:")
            if admin_pass == ADMIN_PASS:
                name=input('Enter Name:').title()
                email=input('Enter email:').lower()
                user_id=user_services.register_librarian(name=name,email=email)
                print(f"Librarian '{name}' has been registered with ID:{user_id}")
            else:
                print('Incorrect Password Try again!')
        elif user_type=='2':
            name=input('Enter Name:').title() 
            email=input('Enter email:').lower()  
            user_id=user_services.register_student(name=name,email=email)
            print(f"Student '{name}' has been registered with ID:{user_id} ")  
        else:
            print('Invaild Choice')   
    except exceptions.UserAlreadyExists as e:
        print(f'Error:{e}')


def manage_book():        
    librarian_id = input("Enter your librarian user ID: ").upper()
    try:
        if user_services.is_librarian(user_id=librarian_id):
            print("1. Add Book")
            print("2.Update Book")
            print("3, Remove book")
            choice = input("Enter your choice: ")
            if choice == '1':
                try:
                 title = input("Enter book title: ")
                 author = input("Enter author name: ")
                 isbn = input("ENter isbn: ")
                 while True:
                   available_copies = input("Enter available_copies: ")
                   if available_copies <=0:
                      print(' At least one copy required')
                   else:
                     book = book_services.add_book(title=title, author=author, isbn=isbn, available_copies=available_copies)
                     print(f"Book '{title}' added with ID: {book[0]}")
                     break
                except ValueError as e:
                    print(f'Error: {e}')
                except exceptions.DuplicateBookISBNError as e:
                    print(f'Error: {e}')
            elif choice == '2':
                book_id = input("Enter book ID:  ")
                try:
                    book = book_services.get_one_book(book_id=book_id)
                    title = input("Enter book title (leave it to keep unchanged): ") or None
                    author = input("Enter author name (leave it to keep unchanged): ") or None
                    isbn = input("ENter isbn (leave it to keep unchanged):  ") or None
                    available_copies = input("Enter available_copies: ") 
                    available_copies = int(available_copies) if available_copies else None
                    update_book = book_services.update_book(book_id=book_id, title=title, author=author, isbn=isbn, available_copies=available_copies)

                    if book:
                        print(f'Book ID: {book_id} has been updated!!')
                        print(f'Updated book details are:\n')

                        #Determine column widths dynamically
                        col_width = [max(len(str(update_book[0])), len("BOOK ID")), #BOOK ID
                                     max(len(str(update_book[1])), len("TITLE")),   #TITLE
                                     max(len(str(update_book[2])), len("AUTHOR")),  #AUTHOR
                                     max(len(str(update_book[4])) if update_book[4] else len("Out of Stock"), len("AVAILABLE COPIES"))]
                        
                        #print header with dynamic spacing
                        print(
                            f"('BOOK ID'.ljust(col_widths[0])) "
                            f"('TITLE'.ljust(col_widths[1])) "
                            f"('AUTHOR'.ljust(col_widths[2])) "
                            f"('AVAILABLE COPIES'.ljust(col_widths[3])) "
                        )
                        print("-" * (sum(col_width) + 6))  #separator adjusts dynamically

                        #print updated book details with proper alignment
                        available_copies = update_book[4] if update_book[4] else "Out of Stock"
                        print(
                            f"{str(update_book[0]).ljust(col_width[0])} "
                            f"{(update_book[1]).ljust(col_width[1])} "
                            f"{(update_book[2]).ljust(col_width[2])} "
                            f"{available_copies.ljust(col_width[3])} "
                        )
                    else:
                        print('No fields provided to update')
                except ValueError as e:
                    print(f'Error: {e}')
                except exceptions.BookNotFound as e:
                    print(f'Error: {e}')
            elif choice == '3':
                try:
                    book_id = int(input("Enter book ID: "))
                    book = book_services.get_one_book(book_id=book_id)
                    book_services.remove_book(book_id=book_id)
                    print(f'Book ID: {book_id} has been removed!!')
                except ValueError as e:
                    print(f'Error: {e}')
                except exceptions.BookNotFound as e:
                    print(f'Error: {e}')
        else:
            print('Invalid choice')
    except exceptions.UserNotFound as e:
        print(f'Error: {e}')







def borrow_book():
    student_id = input("Enter your student ID: ").upper()
    try:
        if user_services.is_student(user_id=student_id):
        
               display_books()
               book_id = input("Enter book ID to borrow: ")
               if book_services.is_available(book_id):
                   book = book_services.get_one_book(book_id = book_id)
                   transactions = transaction_services.get_transaction_by_user_book(student_id, book_id)
               if transactions:
                  for transaction in transactions:
                    if book_id == transaction[2]:
                        if not transaction_services.is_returned(transaction_id=transaction[0]):
                            print("You have already borrowed '{book[1]}' book on {transaction[3]}")
                            return
                        else:
                            transaction_id = transaction_services.borrow_book(user_id=student_id,book_id=book_id)
                            
                            print("Book '{book[1]}' successfully borrowed by '{student_id}' transaction id is: " + transaction_id)
                    else:
                          transaction_id = transaction_services.borrow_book(user_id=student_id, book_id=book_id) 
                          
                          print("Book ''{book[1]}' successfully borrowed by student ID: " + student_id + " transaction id is: " + transaction_id)
                
        else:
             print('Only student can borrow the book!!!')
    except exceptions.UserNotFound as e:
         print(f'Error : {e}')
    except exceptions.BookNotFound as e:
         print(f'Error : {e}')

              
           
                 
                
              
def return_book():
    try:
        transaction_id = int(input("Enter transaction id to return the book: "))
        if not transaction_services.is_returned(transaction_id):
            returned_transaction = transaction_services.return_book(transaction_id= transaction_id)
            book = book_services.get_one_book(book_id=returned_transaction[0])
            print(f"Book '{book[1]}' returned on '{returned_transaction[1]}'")
        else:
            print('Book already returned')
    except ValueError as e:
        print(f"Error: {e}")
    except exceptions.TransactionNotFound as e:
        print(f"Error: {e}")




def display_books():
    """Display all the details"""
    books = book_services.get_all_books()
    if not books:
             print("OOPs!! library doesnot have any book , visit later")
             return
    valid_books = [book for book in books if len(book) == 5]
    if not valid_books:
         print('Error :Inavild book data format')
         return
    headers = ("Book ID", "TITLE", "AUTHOR", "ISBN", "AVAILABLE COPIES")
    sample_entry = [(None, headers[1], None, None, None)]
    col_widths = [
    max(len(str(book[0])) for book in valid_books + [(headers[0], "","","","")]),
    max(len(str(book[1])) for book in valid_books + sample_entry),
    max(len(str(book[2])) for book in valid_books + [(None, None, headers[2], None, None)]),
    max(len(str(book[3])) for book in valid_books + [(None, None, headers[2], None, None)]),
    max(len("Out of Stock"), max(len(str(book[4])) for book in valid_books))
    ]
    print(f"{headers[0].ljust(col_widths[0])}"
          f"{headers[1].ljust(col_widths[1])}"
          f"{headers[2].ljust(col_widths[2])}"
          f"{headers[3].ljust(col_widths[3])}"
          f"{headers[4].ljust(col_widths[4])}")
    print("-" * (sum(col_widths) + 8))
    for book in valid_books:
        available_copies = "Out of stock" if book[4] == 0 else str(book[4])
        print(f"{str(book[0]).ljust(col_widths[0])}"
              f"{book[1].ljust(col_widths[0])}"
              f"{book[2].ljust(col_widths[0])}"
              f"{book[3].ljust(col_widths[0])}"
              f"{available_copies.ljust(col_widths[4])}")
        


def display_transaction_by_id():
    """Display all transactions details using ID"""
    try:
        transaction_id = int(input("Enter transaction ID to see the details: "))
        transaction = transaction_services.get_transaction_by_id(transaction_id)

        if transaction:
            col_widths = [
                max(len(str(transaction[0])), len("TRANSACTION ID")),
                max(len(str(transaction[1])), len("USER ID")),
                max(len(str(transaction[2])), len("BOOK ID")),
                max(len(str(transaction[3])), len("BORROWED DATE")),
                max(len(str(transaction[4])) if transaction[4] else len("Not returned"), len("RETURNED DATE"))
            ]
            print(
                f"{'TRANSACTION ID'.ljust(col_widths[0])}"
                f"{'USER ID'.ljust(col_widths[1])}"
                f"{'BOOK ID'.ljust(col_widths[2])}"
                f"{'BORROWED DATE'.ljust(col_widths[3])}"
                f"{'RETURNED DATE[4]'.ljust(col_widths[4])}"
            )
            print("-"* (sum(col_widths) +8))

            returned_date = transaction[4] if transaction[4] else "Not returned"
            print(
                f"{str(transaction[0]).ljust(col_widths[0])} "
                f"{str(transaction[1]).ljust(col_widths[1])} "
                f"{str(transaction[2]).ljust(col_widths[2])} "
                f"{str(transaction[3]).ljust(col_widths[3])} "
                f"{returned_date.ljust(col_widths[4])}"
            )
        else:
            print(f'No transaction found with ID {transaction_id}')
    except ValueError as e:
        print("Transaction ID should be an integer.",e)
    except exceptions.TransactionsNotFound as e:
        print(f"Error: {e}")
            

def display_transaction_by_user_id():
    """Displays all transactions for a given User ID"""
    try:
        user_id = input("Enter your user ID: ").upper()
        if user_services.is_student(user_id):
            transaction = transaction_services.get_transaction_by_user_id(user_id)
            if transaction:
                #Determine column widths dynamically
                col_widths = [
                    max(len(str(transaction[0])) for transaction in transaction + [("TRANSACTION ID", "", "", "")]),  # TRANSACTION ID
                    max(len(str(transaction[1])) for transaction in transaction + [("", "BOOK ID", "", "")]),  # BOOK ID
                    max(len(str(transaction[2])) for transaction in transaction + [("", "", "BORROWED DATE", "")]),  # BORROWED DATE
                    max(len(str(transaction[3])) if transaction[3] else len("Not returned") for transaction in
                        transaction + [("", "", "", "RETURNED DATE")])  # RETURNED DATE
                ]

                # Print header with dynamic spacing
                print(
                    f"{'TRANSACTION ID'.ljust(col_widths[0])} "
                    f"{'BOOK ID'.ljust(col_widths[1])} "
                    f"{'BORROWED DATE'.ljust(col_widths[2])} "
                    f"{'RETURNED DATE'.ljust(col_widths[3])} "
                )
                print("-" * (sum(col_widths)+ 8)) #Dynamic separator length
            else:
                print(f"No transaction found for User ID (user_id)")
        else:
            print(f'Only Students will have transaction details ')
    except exceptions.UserNotFound as e:
        print(f"Erros: {e}")

           

def main():
    print("\n\n")
    loader("Loading library hub",2)
    print("--Welcome to the Library Hub---")
    dot_loader("Establishing Connection", 3)
    establish_connection()
    establish_connection()
    try:
      while True:
        choice = main_menu()
        if choice == "1":
            user_registration()
        elif choice == "2":
            manage_book()
        elif choice == "3":
            borrow_book()
        elif choice == "4":
            return_book()
        elif choice == "5":
            display_books()
        elif choice == "6":
            display_transaction_by_id()
        elif choice == "7":
            display_transaction_by_user_id()
        elif choice == "8":
            dot_loader("Closing connection", 3)
            break_connection()
            print("Closed Connection")
            # loader("Exiting Library Hub", 2)
            print("Thank You!, Visit Again!")
            break
        else:
            print('Invalid choice')
    except KeyboardInterrupt:
        dot_loader("Closing Connection")
        break_connection()
        print("Closed Connection")
        print("Thank You!, Visit Again!")


if __name__ == "__main__":
    main()



# user_service = UserServices( 'library.db')
# try:
#     print('ID', user_service.register_librarian('zoya','zoya@gmail.com'))
# except exceptions.UserAlreadyExists as e:
#     print(f'error:{e}')
# user_service.close_connection()

# user_service = UserServices( 'library.db')
# try:
#     print('ID', user_service.register_librarian('zoya','z@gmail.com'))
# except exceptions.UserAlreadyExists as e:
#     print(f"Error:{e}")
#     user_service.close_connection()

# user_service = UserServices('library.db')
# try:
#     print('User Data', user_service.get_user(user_id='LBZO04'))
# except exceptions.UserNotFound as e:
#     print(f' Error: {e}')
# user_service.close_connection()

# User_Services=UserServices('library.db')
# try:
#     print(User_Services.is_student('LBZO04'))
# except exceptions.UserAlreadyExists as e:
#     print(f"error:{e}")
# User_Services.close_connection()

# User_Services=UserServices('library.db')
# try:
#     print(User_Services.is_librarian('LBZO04'))
# except exceptions.UserAlreadyExists as e:
#     print(f"error:{e}")
# User_Services.close_connection()

# book_Services=BookServices('library.db')
# try:
#     print(book_Services.get_one_book(2))
# except exceptions.BookNotFound as e:
#     print(f"error:{e}")
# book_Services.close_connection()

# book_Services=BookServices('library.db')
# try:
#     print(book_Services.add_book('python the great','pooja',17326347474,1))
# except exceptions.DuplicateBookISBNError as e:
#     print(f"error:{e}")
# book_Services.close_connection()

# book_Services=BookServices('library.db')
# try:
#    book=book_Services.get_one_book(book_id='4')
#    book=book_Services.update_book(book[0],author='chinnu')
#    if book:
#         print(book)
#    else:
#         print('you fool you have not provided any fields to update ')

# except exceptions.BookNotFound as e:
#     print(f"error:{e}")
# book_Services.close_connection()
######################################################################################

# book_Services=BookServices('library.db')
# try:
#     book=book_Services.get_one_book(book_id=4)
#     print(book_Services.remove_book(book_id=book[0]))
# except exceptions.BookNotFound as e:
#     print(f"error:{e}")
# book_Services.close_connection()


######################################################################################
# book_services = BookServices('library.db')
# try:
#     print(book_services.is_available(2))
# except exceptions.BookNotFound as e:
#     print (f'Error: {e}')
# book_services.close_connection()



# transaction_services = TransactionServices('library.db')
# try:
#     print(transaction_services.get_transaction_by_id(5))
# except exceptions.TransactionNotFound as e:
#     print(f' Error: {e}')
# transaction_services.close_connection()



# transaction_services = TransactionServices(' library.db')
# try:
#     print(transaction_services.get_transaction_by_user_id('STDJ01'))
# except exceptions.UserNotFound as e:
#     print(f' Error: {e}')
# transaction_services.close_connection()



# transaction_services=TransactionServices('library.db')
# try:
#     print(transaction_services.borrowed_date(user_id='STZO03',book_id=2))
# except exceptions.UserNotFound as e:
#     print(f'error:{e}')
# except exceptions.BookNotFound as e:
#     print(f'error:{e}')
# transaction_services.close_connection()

# transaction_services=TransactionServices('library.db')
# try:
#     print(transaction_services.return_book(user_id='STDJ01',book_id=3))
# except exceptions.BookNotFound as e:
#     print(f'error:{e}')
# transaction_services.close_connection()
# def borrow_book(self):
#     transaction_services = TransactionServices("library.db")
#     try:
#         user_id = "STD01"
#         book_id = 2
#         transactions = transaction_services.get_transaction_by_user_id(user_id)
#         for transaction in transactions:
#             if book_id == transaction[1]:
#                 if not transaction_services.is_returned(transaction_id=transaction[0]):
#                     print("You have already borrowed the book")
#                     return
#         print(transaction_services.borrow_book(
#             user_id=user_id,
#             book_id=book_id
#         ))
#     except exceptions.UserNotFound as e:
#         print(f"Error: {e}")
#     except exceptions.BookNotFound as e:
#         print(f"Error: {e}")
#     transaction_services.close_connection()


# transaction_services = TransactionServices("Library.db")
# try:
#     if not transaction_services.is_returned(2):
#         print(transaction_services.return_book(2))
#     else:
#         print('Book already returned')
# except ValueError as e:
#     print(f'Error: {e}')
# #except exceptions.TransactionNotFound as e:
#     print(f'Error: {e}')
# #transaction_services.close_connection()