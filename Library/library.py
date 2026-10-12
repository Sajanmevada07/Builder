
from datetime import datetime

class Book:

    def __int__(self, isbn: str , title: str , author:str):
        self.isbn = isbn
        self.title = title
        self.author = author
        self._is_borrowed: bool = False


        pass

    @property
    def is_borrowed(self):

        return self._is_borrowed

    def mark_as_borrowed(self):

        if self._is_borrowed:
            return False

        self._is_borrowed = True
        return True

    def mark_as_returned(self):

        if not self._is_borrowed:
            return False
        self._is_borrowed = False
        return True 

    def __str__(self):
        status = "Borrowed" if self._is_borrowed  else "Available"

        return f"[{self.isbn}] '{self.title}' by '{self.author} ({status})'"


    def __repr__(self):

        return f"Book(isbn='{self.isbn}', title = '{self.title}')"
            

class Member:

    def __init__(self, Member_id:str, Name:str, Max_books: int = 5):
        self.MemberID = Member_id
        self.Name = Name
        self.Max_books = Max_books
        self._borrowed_books : dict[str, Book] = {}

    @property
    def borrowed_books(self):

        return list[self._borrowed_books.values()]

    def can_borrow(self):
        return len(self._borrowed_books) < self.Max_books

    def add_book(self, book: Book):

        if self.can_borrow() and book.isbn not in self.borrowed_books():
            self.borrowed_books[book.isbn] = book
            return True
        return False

    def remove_book(self, isbn: str):
        return self.borrowed_books.pop(isbn,None)

    def __str__(self):

        return f"Member : {self.name} (ID:{self.MemberID}) - Borrowed: {len(self.borrowed_books)}/{self.Max_books} "



class Transaction:
    def __init__(self, member_id: str, isbn: str, action: str):
        self.transaction_id = id(self)
        self.member_id = member_id
        self.isbn = isbn
        self.action = action  # "BORROW" or "RETURN"
        self.timestamp = datetime.now()

    def __str__(self) -> str:
        time_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"[{time_str}] Member {self.member_id} -> {self.action} -> Book {self.isbn}"

    

