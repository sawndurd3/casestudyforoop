import json
from abc import ABC, abstractmethod
from staff_assignment import staff_assignment

class LibraryItem(ABC):
    _item_count = 0  # Tracks total count of all items in the library
    item_count_file = 'item_count.json'  # File to save the item count

    def __init__(self, title, item_type, publication_year, language, shelf_location, condition):
        self._title = title
        self._item_type = item_type
        self.available = True
        self.staff = staff_assignment[item_type][title]
        self.publication_year = publication_year
        self.language = language
        self.shelf_location = shelf_location
        self.condition = condition

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

    # New Class Methods
    @classmethod
    def add_item(cls, item_type, title, details):
        if item_type in staff_assignment:
            staff_assignment[item_type][title] = details
            cls.increment_item_count()
        else:
            print("Invalid item type.")

    @classmethod
    def remove_item(cls, item_type, title):
        if item_type in staff_assignment and title in staff_assignment[item_type]:
            del staff_assignment[item_type][title]
            cls.decrement_item_count()
        else:
            print("Item not found.")

    @classmethod
    def search_item(cls, item_type, title):
        if item_type in staff_assignment:
            return staff_assignment[item_type].get(title, "Item not found.")
        return "Invalid item type."

    @classmethod
    def get_all_items(cls):
        return staff_assignment


class Book(LibraryItem):
    def __init__(self, title, author, genre, ISBN, pages, publication_year, language, shelf_location, condition):
        super().__init__(title, "Book", publication_year, language, shelf_location, condition)
        self._author = author
        self._genre = genre
        self.ISBN = ISBN
        self.pages = pages

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
        return (f"Book Title: {self._title}\nAuthor: {self._author}\nGenre: {self._genre}\n"
                f"ISBN: {self.ISBN}\nPages: {self.pages}\nPublication Year: {self.publication_year}\n"
                f"Language: {self.language}\nShelf Location: {self.shelf_location}\nCondition: {self.condition}")


class DVD(LibraryItem):
    def __init__(self, title, director, genre, duration, publication_year, language, shelf_location, condition):
        super().__init__(title, "DVD", publication_year, language, shelf_location, condition)
        self._director = director
        self._genre = genre
        self.duration = duration

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
        return (f"DVD Title: {self._title}\nDirector: {self._director}\nGenre: {self._genre}\n"
                f"Duration: {self.duration}\nPublication Year: {self.publication_year}\n"
                f"Language: {self.language}\nShelf Location: {self.shelf_location}\nCondition: {self.condition}")


class Magazine(LibraryItem):
    def __init__(self, title, issue, issue_number, publication_year, language, shelf_location, condition):
        super().__init__(title, "Magazine", publication_year, language, shelf_location, condition)
        self._issue = issue
        self.issue_number = issue_number

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
        return (f"Magazine Title: {self._title}\nIssue: {self._issue}\nIssue Number: {self.issue_number}\n"
                f"Publication Year: {self.publication_year}\nLanguage: {self.language}\nShelf Location: {self.shelf_location}\nCondition: {self.condition}")
