from abc import ABC, abstractmethod

class LibraryItem(ABC):
    _item_count = 0 

    def __init__(self, title, item_type):
        self.__title = title 
        self._item_type = item_type 
        self.available = True 
        LibraryItem._item_count += 1 

    @abstractmethod
    def check_out(self):
        pass

    @abstractmethod
    def return_item(self):
        pass

    @staticmethod
    def total_items():
        return LibraryItem._item_count

class Book(LibraryItem):
    def __init__(self, title, author, pages):
        super().__init__(title, "Book")
        self.__author = author  
        self.__pages = pages  

    def check_out(self):
        if self.available:
            self.available = False
            print(f'Book "{self._item_type}" checked out.')
        else:
            print(f'Book "{self._item_type}" is not available.')

    def return_item(self):
        self.available = True
        print(f'Book "{self._item_type}" returned.')

    def __init__(self, title, director, duration):
        super().__init__(title, "DVD")
        self._director = director  
        self._duration = duration 

    def check_out(self):
        if self.available:
            self.available = False
            print(f'DVD "{self._item_type}" checked out.')
        else:
            print(f'DVD "{self._item_type}" is not available.')

    def return_item(self):
        self.available = True
        print(f'DVD "{self._item_type}" returned.')

class Magazine(LibraryItem):
    def __init__(self, title, issue, pages):
        super().__init__(title, "Magazine")
        self.__issue = issue  
        self.__pages = pages  

    def check_out(self):
        if self.available:
            self.available = False
            print(f'Magazine "{self._item_type}" checked out.')
        else:
            print(f'Magazine "{self._item_type}" is not available.')

    def return_item(self):
        self.available = True
        print(f'Magazine "{self._item_type}" returned.')

class Patron:
    patron_count = 0

    def __init__(self, name):
        self.__name = name  
        self.checked_out_items = []  
        Patron.patron_count += 1  

    def borrow_item(self, item):
        if len(self.checked_out_items) < Patron.max_items_allowed():
            if item.available:
                item.check_out()
                self.checked_out_items.append(item)
                print(f'{self.__name} borrowed {item._item_type}.')
            else:
                print(f'{item._item_type} is not available.')
        else:
            print(f'{self.__name} has reached the maximum limit of borrowed items.')

    def return_item(self, item):
        if item in self.checked_out_items:
            item.return_item()
            self.checked_out_items.remove(item)
            print(f'{self.__name} returned {item._item_type}.')
        else:
            print(f'{self.__name} does not have {item._item_type} checked out.')

    @classmethod
    def total_patrons(cls):
        return cls.patron_count

    @staticmethod
    def max_items_allowed():
        return 5  

class LibraryStaff:
    _staff_count = 0  

    def __init__(self, name, staff_id):
        self.__name = name 
        self.staff_id = staff_id 
        LibraryStaff._staff_count += 1  

    def check_out_item(self, patron, item):
        patron.borrow_item(item)

    def check_in_item(self, patron, item):
        patron.return_item(item)

    @staticmethod
    def total_staff():
        return LibraryStaff._staff_count