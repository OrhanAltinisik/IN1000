class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True

    def borrow(self):
        if self.available:
            self.available = False
        else:
            print(self.title + " is already borrowed")

    def give_back(self):
        self.available = True

    def show_info(self):
        if self.available:
            status = "available"
        else:
            status = "borrowed"
        print(self.title + " by " + self.author + " (" + status + ")")


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def find_book(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None

    def show_available(self):
        for book in self.books:
            if book.available:
                book.show_info()


library = Library()
library.add_book(Book("Dune", "Frank Herbert"))
library.add_book(Book("1984", "George Orwell"))
library.add_book(Book("Emma", "Jane Austen"))

found = library.find_book("Dune")
if found is not None:
    found.borrow()

library.show_available()