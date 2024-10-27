import json
from patron import Patron
from library_item import Book, Magazine, DVD, LibraryItem
from staff_assignment import staff_assignment

# Load the staff_assignment.txt data
def load_staff_assignment():
    try:
        with open("staff_assignment.txt", "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Error: staff_assignment.txt file not found.")
        return {}

# Function to search for an item
def search_item(item_type, title):
    staff_assignment = load_staff_assignment()  # Load assignment data

    # Check if the item type exists
    if item_type not in staff_assignment:
        print(f"No items of type '{item_type}' found.")
        return False

    # Check if the title exists within the given item type
    if title in staff_assignment[item_type]:
        item_info = staff_assignment[item_type][title]
        staff = item_info.get("staff")
        station = item_info.get("station")
        
        # Display general information
        print(f"'{title}' ({item_type}) is available.")
        print(f"Assigned to staff: {staff}, Station: {station}")

        # Additional details based on item type
        if item_type == "Book":
            author = item_info.get("author")
            genre = item_info.get("genre")
            print(f"Author: {author}, Genre: {genre}")
        
        elif item_type == "Magazine":
            issue = item_info.get("issue")
            print(f"Issue: {issue}")

        elif item_type == "DVD":
            director = item_info.get("director")
            genre = item_info.get("genre")
            print(f"Director: {director}, Genre: {genre}")
        
        return True

    else:
        print(f"'{title}' ({item_type}) is not available.")
        return False

def borrow_or_return_item(patron):
    while True:
        item_type = input("What type of item would you like to search for? (Book/Magazine/DVD): ").strip()

        # Check if the item type is valid
        if item_type not in staff_assignment:
            print("Invalid item type selected.")
            continue

        title = input(f"Enter the title of the {item_type}: ").strip()

        # Use the search function to check item availability
        if not search_item(item_type, title):
            continue  # Item is not available; prompt user again

        # Confirm if the user wants to borrow/return this item after the search
        action = input("Would you like to borrow or return this item? (borrow/return): ").strip().lower()

        if action not in ["borrow", "return"]:
            print("Invalid action.")
            continue

        # Retrieve specific information from staff_assignment based on the item type
        item_data = staff_assignment[item_type][title]

        if item_type == "Book":
            author = item_data.get("author", "Unknown Author")
            genre = item_data.get("genre", "Unknown Genre")
            item = Book(title, author, genre)
        elif item_type == "Magazine":
            issue = item_data.get("issue", "Unknown Issue")
            item = Magazine(title, issue)
        elif item_type == "DVD":
            director = item_data.get("director", "Unknown Director")
            genre = item_data.get("genre", "Unknown Genre")
            item = DVD(title, director, genre)

        if action == "borrow":
            patron.borrow_item(item)
            print(f"Total items remaining: {LibraryItem.total_items()}")  # Display remaining items after borrowing
        elif action == "return":
            patron.return_item(item)
            print(f"Total items remaining: {LibraryItem.total_items()}")  # Display remaining items after returning

        another_action = input("Would you like to search for another item? (yes/no): ").strip().lower()
        if another_action != "yes":
            print("Saving your borrowing data...")
            patron.save_patron_data()  # Save patron data before exiting
            print("Thank you for using the library system!")
            break

if __name__ == '__main__':
    # Initialize item count based on staff_assignment or previous run
    LibraryItem.initialize_item_count()

    # Print the total number of items in the library
    print(f"Total items in the library: {LibraryItem.total_items()}")

    # Main script
    user_name = input("Please enter your name: ").strip()

    # Load the patron's data if it exists
    patron = Patron.load_patron_data(user_name)

    # Start the borrowing/returning process
    borrow_or_return_item(patron)

    # Save the patron's data when done
    patron.save_patron_data()
