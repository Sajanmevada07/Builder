
from datetime import datetime
from typing import Optional


class Book:
    def __init__(self, isbn: str, title: str, author: str):
        self.isbn = isbn
        self.title = title
        self.author = author
        self._is_borrowed: bool = False

    @property
    def is_borrowed(self) -> bool:
        return self._is_borrowed

    def mark_as_borrowed(self) -> bool:
        if self._is_borrowed:
            return False
        self._is_borrowed = True
        return True

    def mark_as_returned(self) -> bool:
        if not self._is_borrowed:
            return False
        self._is_borrowed = False
        return True

    def __str__(self) -> str:
        status = "Borrowed" if self._is_borrowed else "Available"
        return f"[{self.isbn}] '{self.title}' by {self.author} ({status})"

    def __repr__(self) -> str:
        return f"Book(isbn='{self.isbn}', title='{self.title}')"
            

class Member:
    def __init__(self, member_id: str, name: str, max_books: int = 3):
        self.member_id = member_id
        self.name = name
        self.max_books = max_books
        self._borrowed_books: dict[str, Book] = {}  # ISBN -> Book mapping

    @property
    def borrowed_books(self) -> list[Book]:
        return list(self._borrowed_books.values())

    def can_borrow(self) -> bool:
        return len(self._borrowed_books) < self.max_books

    def add_book(self, book: Book) -> bool:
        if self.can_borrow() and book.isbn not in self._borrowed_books:
            self._borrowed_books[book.isbn] = book
            return True
        return False

    def remove_book(self, isbn: str) -> Optional[Book]:
        return self._borrowed_books.pop(isbn, None)

    def __str__(self) -> str:
        return f"Member: {self.name} (ID: {self.member_id}) - Borrowed: {len(self._borrowed_books)}/{self.max_books}"



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

    

class Library:
    def __init__(self, name: str):
        self.name = name
        self._books: dict[str, Book] = {}       # ISBN -> Book
        self._members: dict[str, Member] = {}   # Member ID -> Member
        self._transactions: list[Transaction] = []

    # --- Management Methods ---
    def add_book(self, book: Book) -> None:
        self._books[book.isbn] = book
        print(f"Added to library: {book.title}")

    def register_member(self, member: Member) -> None:
        self._members[member.member_id] = member
        print(f"Registered member: {member.name}")

    # --- Search Methods ---
    def search_by_title(self, query: str) -> list[Book]:
        return [b for b in self._books.values() if query.lower() in b.title.lower()]

    def search_by_author(self, query: str) -> list[Book]:
        return [b for b in self._books.values() if query.lower() in b.author.lower()]

    # --- Loan Operations ---
    def checkout_book(self, member_id: str, isbn: str) -> bool:
        member = self._members.get(member_id)
        book = self._books.get(isbn)

        if not member:
            print(f"Error: Member ID '{member_id}' not found.")
            return False
        if not book:
            print(f"Error: Book ISBN '{isbn}' not found.")
            return False
        if book.is_borrowed:
            print(f"Error: '{book.title}' is currently checked out.")
            return False
        if not member.can_borrow():
            print(f"Error: {member.name} has reached borrowing limit ({member.max_books} books).")
            return False

        # Execute Transaction
        book.mark_as_borrowed()
        member.add_book(book)
        tx = Transaction(member_id, isbn, "BORROW")
        self._transactions.append(tx)
        print(f"Success: '{book.title}' checked out to {member.name}.")
        return True

    def return_book(self, member_id: str, isbn: str) -> bool:
        member = self._members.get(member_id)
        book = self._books.get(isbn)

        if not member or not book:
            print("Error: Invalid member or ISBN.")
            return False

        if member.remove_book(isbn):
            book.mark_as_returned()
            tx = Transaction(member_id, isbn, "RETURN")
            self._transactions.append(tx)
            print(f"Success: '{book.title}' returned by {member.name}.")
            return True

        print(f"Error: {member.name} does not have book '{isbn}' checked out.")
        return False

    def list_transactions(self) -> None:
        print(f"\n--- {self.name} Transaction Log ---")
        for tx in self._transactions:
            print(tx)



# Initialize Library
city_library = Library("Central City Library")

# Populate Books
b1 = Book("978-0135404676", "Clean Code", "Robert C. Martin")
b2 = Book("978-0201616224", "The Pragmatic Programmer", "Andrew Hunt")
b3 = Book("978-0596009205", "Head First Design Patterns", "Eric Freeman")

city_library.add_book(b1)
city_library.add_book(b2)
city_library.add_book(b3)

# Register Member
m1 = Member("M001", "Alice Vance", max_books=2)
city_library.register_member(m1)

print("\n--- Borrowing Operations ---")
# Check out book 1
city_library.checkout_book("M001", "978-0135404676")

# Check out book 2
city_library.checkout_book("M001", "978-0201616224")

# Attempt to exceed borrowing limit (max_books = 2)
city_library.checkout_book("M001", "978-0596009205")

print("\n--- Member State ---")
print(m1)

print("\n--- Return Operations ---")
city_library.return_book("M001", "978-0135404676")

print("\n--- Final Audit Log ---")
city_library.list_transactions()