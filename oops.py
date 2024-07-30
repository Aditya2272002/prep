class Member:
    def __init__(self, name) -> None:
        self.name = name
        self.book_have = []

    def get_book(self, book):
        if book.book_taken():
            self.book_have.append(book)
            print(f"{self.name} took '{book.title}'")
        else:
            print(f"{self.name} could not take '{book.title}'")

    def return_book(self, book):
        if book in self.book_have:
            book.book_retured()
            self.book_have.remove(book)
            print(f"{self.name} returned '{book.title}'")
        else:
            print(f"{self.name} does not have '{book.title}'")

    def __str__(self):
        books = ", ".join(book.title for book in self.book_have)
        return f"{self.name} has: {books if books else 'No books'}"


class Book:
    def __init__(self, title) -> None:
        self.title = title
        self.available = True

    def book_taken(self):
        if self.available:
            self.available = False
            return True
        return False

    def book_retured(self):
        self.available = True

    def __str__(self):
        return f"'{self.title}' ({'Available' if self.available else 'Checked out'})"


class Library:
    def __init__(self) -> None:
        self.books = []
        self.members = []

    def add_book(self, book):
        self.books.append(book)
        print(f"Added {book} to the library.")

    def add_member(self, member):
        self.members.append(member)
        print(f"Added member: {member.name}")

    def __str__(self):
        books = "\n".join(str(book) for book in self.books)
        members = "\n".join(str(member) for member in self.members)
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
    print(library.__str__())

    # Member actions
    member1.get_book(book1)
    print('--- After Alice takes a book ---')
    print(library.__str__())

    member2.get_book(book1)  # Should fail as book1 is already taken
    print('--- After Bob tries to take the same book ---')
    print(library.__str__())

    member1.return_book(book1)
    print('--- After Alice returns the book ---')
    print(library.__str__())

    member2.get_book(book1)  # Should succeed now
    print('--- After Bob takes the book again ---')
    print(library.__str__())


if __name__ == "__main__":
    main()
