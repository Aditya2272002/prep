from abc import ABC, abstractmethod

# Abstract Base Class for Library Items


class LibraryItem(ABC):
    @abstractmethod
    def __str__(self):
        pass

# Book class implementing LibraryItem


class Book(LibraryItem):
    def __init__(self, title) -> None:
        self.__title = title
        self.__available = True

    def book_taken(self):
        if self.__available:
            self.__available = False
            return True
        return False

    def book_returned(self):
        self.__available = True

    def get_title(self):
        return self.__title

    def set_title(self, title):
        self.__title = title

    def __str__(self):
        return f"'{self.__title}' ({'Available' if self.__available else 'Checked out'})"

# Member class implementing LibraryItem


class Member(LibraryItem):
    def __init__(self, name) -> None:
        self.__name = name
        self.__books = []

    def get_book(self, book):
        if book.book_taken():
            self.__books.append(book)
            print(f"{self.__name} took '{book.get_title()}'")
        else:
            print(f"{self.__name} could not take '{book.get_title()}'")

    def return_book(self, book):
        if book in self.__books:
            book.book_returned()
            self.__books.remove(book)
            print(f"{self.__name} returned '{book.get_title()}'")
        else:
            print(f"{self.__name} does not have '{book.get_title()}'")

    def __str__(self):
        books = ", ".join(book.get_title() for book in self.__books)
        return f"{self.__name} has: {books if books else 'No books'}"

# Library class managing Books and Members


class Library:
    def __init__(self) -> None:
        self.__books = []
        self.__members = []

    def add_book(self, book):
        self.__books.append(book)
        print(f"Added {book} to the library.")

    def add_member(self, member):
        self.__members.append(member)
        # Use __str__() to get member's string representation
        print(f"Added member: {member.__str__()}")

    def __str__(self):
        books = "\n".join(str(book) for book in self.__books)
        members = "\n".join(str(member) for member in self.__members)
        return f"Library Inventory:\n{books}\n\nLibrary Members:\n{members}"


def main():
    # Create a library
    library = Library()

    # Add books to the library
    book1 = Book("1984")
    book2 = Book("To Kill a Mockingbird")
    library.add_book(book1)
    library.add_book(book2)

    # Register members
    member1 = Member("Alice")
    member2 = Member("Bob")
    library.add_member(member1)
    library.add_member(member2)

    # Print initial state
    print('--- Initial State ---')
    print(library)  # Calls library.__str__()

    # Member actions
    member1.get_book(book1)
    print('--- After Alice takes a book ---')
    print(library)  # Calls library.__str__()

    member2.get_book(book1)  # Should fail as book1 is already taken
    print('--- After Bob tries to take the same book ---')
    print(library)  # Calls library.__str__()

    member1.return_book(book1)
    print('--- After Alice returns the book ---')
    print(library)  # Calls library.__str__()

    member2.get_book(book1)  # Should succeed now
    print('--- After Bob takes the book again ---')
    print(library)  # Calls library.__str__()


if __name__ == "__main__":
    main()
