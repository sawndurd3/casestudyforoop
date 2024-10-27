import json
from abc import ABC, abstractmethod
from staff_assignment import staff_assignment

class LibraryItem(ABC):
    _item_count = 0  # Tracks the total count of all items in the library
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
        # General display format for library items
        return f"{self._item_type} - Title: {self._title}"

    @staticmethod
    def total_items():
        return LibraryItem._item_count

    @staticmethod
    def decrement_item_count():
        if LibraryItem._item_count > 0:
            LibraryItem._item_count -= 1
            LibraryItem.save_item_count()  # Save updated item count

    @staticmethod
    def increment_item_count():
        # Increments the count and saves the updated item count to file
        LibraryItem._item_count += 1
        LibraryItem.save_item_count()  # Save updated item count

    @staticmethod
    def initialize_item_count():
        # Try to load the item count from file
        try:
            with open(LibraryItem.item_count_file, 'r') as file:
                LibraryItem._item_count = json.load(file)
            print(f"Loaded item count: {LibraryItem._item_count}")
        except (FileNotFoundError, json.JSONDecodeError):
            # If file is missing or unreadable, initialize from staff_assignment
            LibraryItem._item_count = sum(len(items) for items in staff_assignment.values())
            LibraryItem.save_item_count()  # Save initialized count
            print(f"Initialized item count: {LibraryItem._item_count}")

    @staticmethod
    def save_item_count():
        # Save the current item count to a file
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
            LibraryItem.decrement_item_count()  # Decrement item count when an item is checked out
        else:
            print(f'Book "{self._title}" is not available.')

    def return_item(self):
        self.available = True
        print(f'Book "{self._title}" returned.')
        LibraryItem.increment_item_count()  # Increment the item count

    def __str__(self):
        # Specific display format for books
        return f"Book Title: {self._title}\nAuthor: {self._author}\nGenre: {self._genre}"


class DVD(LibraryItem):
    def __init__(self, title, director, genre):
        super().__init__(title, "DVD")
        self._director = director
        self._genre = genre

    def check_out(self):
        if self.available:
            self.available = False
            LibraryItem.decrement_item_count()  # Decrement item count when an item is checked out
        else:
            print(f'DVD "{self._title}" is not available.')

    def return_item(self):
        self.available = True
        print(f'DVD "{self._title}" returned.')
        LibraryItem.increment_item_count()  # Increment the item count

    def __str__(self):
        # Specific display format for DVDs
        return f"DVD Title: {self._title}\nDirector: {self._director}\nGenre: {self._genre}"


class Magazine(LibraryItem):
    def __init__(self, title, issue):
        super().__init__(title, "Magazine")
        self._issue = issue

    def check_out(self):
        if self.available:
            self.available = False
            LibraryItem.decrement_item_count()  # Decrement item count when an item is checked out
        else:
            print(f'Magazine "{self._title}" is not available.')

    def return_item(self):
        self.available = True
        print(f'Magazine "{self._title}" returned.')
        LibraryItem.increment_item_count()  # Increment the item count

    def __str__(self):
        # Specific display format for magazines
        return f"Magazine Title: {self._title}\nIssue: {self._issue}"


