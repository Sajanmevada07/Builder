


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
            