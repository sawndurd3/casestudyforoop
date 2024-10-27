import json
from abc import ABC, abstractmethod
from staff_assignment import staff_assignment

class LibraryItem(ABC):
    _item_count = 0  # Tracks total count of all items in the library
    item_count_file = 'item_count.json'  # File to save the item count

    def __init__(self, title, item_type):
        self._title = title
        self._item_type = item_type
        self.available = True
        self.staff = staff_assignment[item_type][title]

    @abstractmethod
    def check_out(self):
        pass

    @abstractmethod
    def return_item(self):
        pass

    def __str__(self):
        return f"{self._item_type} - Title: {self._title}"

    @staticmethod
    def total_items():
        return LibraryItem._item_count
        
    @staticmethod
    def increment_item_count():
        LibraryItem._item_count += 1
        LibraryItem.save_item_count()

    @staticmethod
    def decrement_item_count():
        if LibraryItem._item_count > 0:
            LibraryItem._item_count -= 1
            LibraryItem.save_item_count()

    @staticmethod
    def initialize_item_count():
        try:
            with open(LibraryItem.item_count_file, 'r') as file:
                LibraryItem._item_count = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            LibraryItem._item_count = sum(len(items) for items in staff_assignment.values())
            LibraryItem.save_item_count()

    @staticmethod
    def save_item_count():
        with open(LibraryItem.item_count_file, 'w') as file:
            json.dump(LibraryItem._item_count, file)

class Book(LibraryItem):
    def __init__(self, title, author, genre):
        super().__init__(title, "Book")
        self._author = author
        self._genre = genre

    def check_out(self):
        if self.available:
            self.available = False
            LibraryItem.decrement_item_count()
        else:
            print(f'Book "{self._title}" is currently unavailable.')

    def return_item(self):
        if self.available:
            self.available = False
        if not self.available:
            self.available = True
            LibraryItem.increment_item_count()
            print(f'Book "{self._title}" has been returned and is now available.')
        else:
            print(f'Book "{self._title}" was already available')

    def __str__(self):
        return f"Book Title: {self._title}\nAuthor: {self._author}\nGenre: {self._genre}"


class DVD(LibraryItem):
    def __init__(self, title, director, genre):
        super().__init__(title, "DVD")
        self._director = director
        self._genre = genre

    def check_out(self):
        print(f"Attempting to check out DVD '{self._title}'.")
        if self.available:
            self.available = False
            LibraryItem.decrement_item_count()
            print(f'DVD "{self._title}" has been checked out.')
        else:
            print(f'DVD "{self._title}" is currently unavailable.')

    def return_item(self):
        if self.available:
            self.available = False
        if not self.available:
            self.available = True
            LibraryItem.increment_item_count() 
            print(f'DVD "{self._title}" has been returned and is now available.')
        else:
            print(f'DVD "{self._title}" was already available')

    def __str__(self):
        return f"DVD Title: {self._title}\nDirector: {self._director}\nGenre: {self._genre}"


class Magazine(LibraryItem):
    def __init__(self, title, issue):
        super().__init__(title, "Magazine")
        self._issue = issue

    def check_out(self):
        print(f"Attempting to check out Magazine '{self._title}'.")
        if self.available:
            self.available = False
            LibraryItem.decrement_item_count()
            print(f'Magazine "{self._title}" has been checked out.')
        else:
            print(f'Magazine "{self._title}" is currently unavailable.')

    def return_item(self):
        if self.available:
            self.available = False
        if not self.available:
            self.available = True
            LibraryItem.increment_item_count()  
            print(f'\nMagazine "{self._title}" has been returned and is now available.')
        else:
            print(f'Magazine "{self._title}" was already available')

    def __str__(self):
        return f"Magazine Title: {self._title}\nIssue: {self._issue}"
