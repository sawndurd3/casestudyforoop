import json
import datetime
from borrowing_data import append_borrowing_data, delete_borrowing_data
from library_item import Book, Magazine, DVD
from staff_assignment import staff_assignment

class Patron:
    patrons_data_file = 'patrons_data.json'
    patron_count = 0

    def __init__(self, name):
        self.__name = name
        self.checked_out_items = []  # Stores LibraryItem objects
        self.borrowed_count = 0  # Initialize borrowed count
        self.load_patron_count()

        # Increment the patron count only if it's a new patron
        if not self.is_existing_patron():
            Patron.patron_count += 1

    def load_patron_count(self):
        try:
            with open(Patron.patrons_data_file, 'r') as file:
                patrons_data = json.load(file)
                if 'patron_count' in patrons_data:
                    Patron.patron_count = patrons_data['patron_count']
        except FileNotFoundError:
            Patron.patron_count = 0  # Initialize to 0 if the file doesn't exist

    def is_existing_patron(self):
        try:
            with open(Patron.patrons_data_file, 'r') as file:
                patrons_data = json.load(file)
                return self.__name in patrons_data
        except FileNotFoundError:
            return False  # If the file doesn't exist, this is a new patron

    def borrow_item(self, item):
        # Check if the item is already borrowed by the patron
        item_already_borrowed = any(
            i._title == item._title and i._item_type == item._item_type for i in self.checked_out_items
        )

        if item_already_borrowed:
            print(f"{self.__name} has already borrowed '{item._title}'. Cannot borrow the same item twice.")
            return  # Exit the function if the item is already borrowed

        if len(self.checked_out_items) < Patron.max_items_allowed():
            if item.available:
                staff_info = staff_assignment[item._item_type][item._title]
                staff_name = staff_info["staff"]
                staff_station = staff_info["station"]
                # Check out the item and append it to the patron's checked-out items
                item.check_out()
                self.checked_out_items.append(item)
                self.borrowed_count += 1  # Increment borrowed count when borrowing

                # Print structured output with simplified information
                print(f"\n{self.__name} borrowed a {item._item_type}.")
                print(item)
                print(f"This {item._item_type} is handled by {staff_name}. Go to station {staff_station} to check out.\n")

                # Log borrowing data
                date_borrowed = datetime.date.today()
                due_date = date_borrowed + datetime.timedelta(days=30)
                append_borrowing_data(self.__name, item._title, date_borrowed, due_date, item._item_type)
            else:
                print(f'{item._item_type} is not available.')
        else:
            print(f'{self.__name} has reached the maximum limit of borrowed items.')

    def return_item(self, item):
        # Check if the item is in the patron's checked-out items
        item_found = any(i._title == item._title and i._item_type == item._item_type for i in self.checked_out_items)

        if item_found:
            item.return_item()  # Call return_item on the item to mark it as returned
            self.checked_out_items = [i for i in self.checked_out_items if not (i._title == item._title and i._item_type == item._item_type)]

            self.borrowed_count -= 1  # Decrement the borrowed count when an item is returned
            
            print(f'{self.__name} returned a {item._item_type}.')
            delete_borrowing_data(self.__name, item._title, item._item_type)
        else:
            print(f'\n{self.__name} does not have {item._item_type} checked out.')

    @classmethod
    def total_patrons(cls):
        return cls.patron_count

    @staticmethod
    def max_items_allowed():
        return 5

    def save_patron_data(self):
        try:
            with open(Patron.patrons_data_file, 'r') as file:
                patrons_data = json.load(file)
        except FileNotFoundError:
            patrons_data = {}

        # Save the patron's current checked out items
        patrons_data[self.__name] = [{
            "title": item._title, 
            "type": item._item_type,
            "publication_year": item.publication_year,
            "language": item.language,
            "shelf_location": item.shelf_location,
            "condition": item.condition
        } for item in self.checked_out_items]

        # Prepare a new dictionary to maintain order
        ordered_data = {'patron_count': Patron.patron_count}  # Start with the patron_count at the top

        # Add existing patrons after the patron_count
        for patron in patrons_data:
            if patron != 'patron_count':  # Skip the existing patron_count entry if it exists
                ordered_data[patron] = patrons_data[patron]

        # Save the new ordered data with pretty printing
        with open(Patron.patrons_data_file, 'w') as file:
            json.dump(ordered_data, file, indent=4)  # Indent for better readability

    @classmethod
    def load_patron_data(cls, name):
        try:
            with open(cls.patrons_data_file, 'r') as file:
                patrons_data = json.load(file)
                
                # Check if the patron name exists in the loaded data
                if name in patrons_data:
                    patron = cls(name)
                    
                    # Ensure we correctly access the list of borrowed items
                    for item_data in patrons_data[name]:
                        title = item_data["title"]
                        item_type = item_data["type"]
                        
                        # Retrieve additional attributes if available
                        publication_year = item_data.get("publication_year", "Unknown")
                        language = item_data.get("language", "English")
                        shelf_location = item_data.get("shelf_location", "General")
                        condition = item_data.get("condition", "Good")
                        
                        # Create the corresponding item based on the type
                        if item_type == "Book":
                            item = Book(title, "Unknown Author", "Unknown Genre", "N/A", 0,
                                        publication_year, language, shelf_location, condition)
                        elif item_type == "Magazine":
                            item = Magazine(title, "Unknown Issue", 0,
                                            publication_year, language, shelf_location, condition)
                        elif item_type == "DVD":
                            item = DVD(title, "Unknown Director", "Unknown Genre", 0,
                                       publication_year, language, shelf_location, condition)
                        else:
                            print(f"Unknown item type: {item_type}.")
                            continue  # Skip unknown item types
                        
                        patron.checked_out_items.append(item)
                    return patron

        except FileNotFoundError:
            print("Patron data file not found. A new patron will be created.")
        except json.JSONDecodeError:
            print("Error decoding JSON. Please check the file format.")
        
        return cls(name)  # Return a new patron if no data is found or on error
