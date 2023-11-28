import re
import pandas
import tabulate

#========The beginning of the class==========
class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = float(cost)
        self.quantity = int(quantity)

    def get_cost(self):
        # Code to return the cost of the shoe in this method.
        return self.cost

    def get_quantity(self):
        # Code to return the quantity of the shoes.
        return self.quantity

    def __str__(self):
        # Code to returns a string representation of a class.
        return f'''
Country: {self.country} 
Code: {self.code}
Product: {self.product}
Cost: {self.cost}
Quantity: {self.quantity}'''

#=============Shoe list===========
# This list will be used to store a list of objects of shoes.
shoe_list = []
#==========Functions outside the class==============
def read_shoes_data():
    shoe_list.clear()
    try:
        with open("inventory.txt", "r", encoding="utf-8") as file:
            # Skip the first (header) line of the text file (1)
            next(file)
            # For each line in the file, split into a list of words
            for line in file:
                shoe_obj = line.replace("\n", "").split(",")
                try:
                    shoe_obj = Shoe(shoe_obj[0], shoe_obj[1], shoe_obj[2], shoe_obj[3], shoe_obj[4])
                    shoe_list.append(shoe_obj)
                # If a line was not formatted correctly, prints an error
                # message and quits the program
                except IndexError:
                    print("Sorry, an item in \"inventory.txt\" was not \
formatted correctly. Please ensure that each item is formatted in the \
following way : \"country,code,product,cost,quantity\" with no empty lines \
between products.")
                    quit()
    # If the file cannot be found, give an error message and exit the program
    except FileNotFoundError:
        print("Sorry, the inventory.txt file cannot be found. Please make \
that it is in the folder and restart the program.")
        quit()


def capture_shoes():
    '''
    This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object inside the shoe list.
    '''
    country = input("Please enter the country this shoe is stocked in:\n")
    while True:
        try:
            code = input("Please enter the code of the product:\n").upper().\
                replace(" ", "")
            # If code is not the format "SKU" then 5 numbers (SKUXXXXX), raise
            # an error (2)
            if re.match(r"^SKU\d{5}$", code) is None:
                raise TypeError
        # If a TypeError is raised, asks user to try again
        except TypeError:
            print(f"The product code \"{code}\" you entered is invalid. \
Please ensure that your code is entered as follows and try again: \
\"SKUXXXXX\" where X's are digits from 0-9.")
            continue
        else:
            break
    product = input("Please enter the name of the product:\n")
    # Loops until user enters a valid response (3)
    while True:
        try:
            cost = float(input("Please enter the cost of the product, omitting\
 the currency:\n").replace(" ", ""))
        # If the user enters anything other than a number, give an error
        # message and let them try again.
        except ValueError:
            print("You can only enter a number. Please remember to omit the \
currency symbol and try again.")
            continue
        else:
            break
    while True:
        try:
            quantity = int(input("Please enter the quantity of this product in\
 stock:\n").replace(" ", ""))
        except ValueError:
            print("You can only enter a integer. Please try again.")
        else:
            break
    # Creates a shoe object from the inputs provided
    shoe_obj_2 = Shoe(country, code, product, cost, quantity)
    # Adds the new shoe to inventory.txt file
    with open("inventory.txt", "a", encoding="utf-8") as shoe_data:
        shoe_data.writelines(f"\n{country},{code},{product},{cost},{quantity}")
    shoe_list.append(shoe_obj_2)
    print("Shoe has been successfully added. Returning to menu.")


def view_all():
    '''
    This function will iterate over the shoes list and
    print the details of the shoes returned from the __str__
    function. Optional: you can organise your data in a table format
    by using Python’s tabulate module.
    '''
     # Calls the read_shoes_data function to reread the inventory.txt
    read_shoes_data()
    # Creates an empty list for storing shoe objects as dictionaries
    shoes_dict_list = []
    # For each shoe in the list, appends the dictionary of an object to the
    # list (4)
    for shoe in shoe_list:
        shoes_dict_list.append(shoe.__dict__)
    # Converts the dictionary to a dataframe (5)
    shoes_dataframe = pandas.DataFrame(shoes_dict_list)
    # Capitalises the first letter of each of the headers (6)
    shoes_dataframe.columns = map(str.capitalize, shoes_dataframe.columns)
    # Creates a table from the shoes dataframe (7) and prints it
    table = tabulate.tabulate(shoes_dataframe, headers="keys",
                              tablefmt="fancy_grid")
    print(table)


# I am defining this function for later use in my program.
# It finds the product with the lowest amount of stock from the shoe_list.
def find_lowest_stock():
    # Creates an empty list for storing shoe quantities.
    shoe_quantity = []
    # Iterates through the shoe_list and adds the quantity to shoe_quantity list.
    for shoe in shoe_list:
        shoe_quantity.append(shoe.get_quantity())
    # Finds the lowest value in quantity list.
    lowest_stock_quantity = min(shoe_quantity)
    # Finds the index of the lowest value stock and assigns it a global variable.
    for shoe in shoe_list:
        if lowest_stock_quantity == shoe.quantity:
            global lowest_stock_index
            lowest_stock_index = shoe_list.index(shoe)
    global lowest_quantity_product
    lowest_quantity_product = shoe_list[lowest_stock_index]


# I am defining this function for later use in my program.
# It finds the product with the highest amount of stock from the shoe_list.
def find_highest_stock():   
    shoe_quantity = []
    
    for shoe in shoe_list:
        shoe_quantity.append(shoe.get_quantity())
    highest_stock_quantity = max(shoe_quantity)

    for shoe in shoe_list:
        if highest_stock_quantity == shoe.quantity:
            global highest_stock_index
            highest_stock_index = shoe_list.index(shoe)
    global highest_quantity_product
    highest_quantity_product = shoe_list[highest_stock_index]


def re_stock():
    '''
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Ask the user if they
    want to add this quantity of shoes and then update it.
    This quantity should be updated on the file for this shoe.
    '''
    find_lowest_stock()
    # Prints a statement telling the user the product with the lowest stock and
    # ask if they want to restock it
    print(f"{lowest_quantity_product.product} has the least stock \
({lowest_quantity_product.quantity}). Would you like to restock it? (y/n)")
    restock_response = input("Enter your selection here:").lower()\
        .replace(" ", "")
    # If they answer y or yes, ask how much they want to restock
    if restock_response == "y" or restock_response == "yes":
        while True:
            try:
                restock_amount = int(input("Please enter the amount you would like to restock:"))
                # Adds the restock amount to the old stock
                new_stock = (lowest_quantity_product.quantity + restock_amount)
                file_data_string = ""
                # Opens the inventory.txt file
                with open("inventory.txt", "r") as file_data:
                    # Writes shoes_data to a new string by line
                    for line in file_data:
                        file_data_string += line
                    # Splits the new string into a list of lines
                    file_data_string = file_data_string.split("\n")
                    # Creates a variable for the shoe to restock with the index
                    # of the lowest quantity shoe
                    restocked_shoe = file_data_string[lowest_stock_index + 1]
                    # Splits the restocked shoe into a list of words
                    restocked_shoe = restocked_shoe.split(",")
                    # Replaces the quantity of the lowest quantity shoe with
                    # the new quantity after restock
                    restocked_shoe[4] = str(new_stock)
                    # Joins the restocked shoe list back together
                    restocked_shoe = ",".join(restocked_shoe)
                    # Replaces the line in the string of shoe data with the
                    # restocked shoe amount
                    file_data_string[lowest_stock_index + 1] = restocked_shoe
                    # Rejoins the shoes_data string so that it can be written
                    # to file
                    file_data_string = "\n".join(file_data_string)
                # Writes the shoes_data_string to file
                with open("inventory.txt", "w") as file_data:
                    file_data.writelines(file_data_string)
                # Prints a confirmation
                print(f"{lowest_quantity_product.product} has been \
successfully restocked. New stock is {new_stock}.")
            # If the user doesn't enter an integer, allows them to try
            # again
            except ValueError:
                print("You can only enter anumber. Please try again.")
                continue
            else:
                break
    # If the user enters n or no, returns to menu
    elif restock_response == "n" or restock_response == "no":
        print("Returning to menu...")
    # Otherwise, gives an error message and allows the user to try again.
    else:
        print("Your input is invalid. Please try again.")
        re_stock()


def search_shoe():
    '''
     This function will search for a shoe from the list
     using the shoe code and return this object so that it will be printed.
    '''
    searched_shoe = None
    # Getting input from the user for the product code of the shoe they want to search.
    while True:
        try:
            user_input = input("Enter the product code of the shoe you would like to search: ").upper().replace(" ", "")
            # If code is not the format "SKU" then 5 numbers (SKUXXXXX), raise an error.
            if re.match(r"^SKU[0-9][0-9][0-9][0-9][0-9]\Z", user_input) is None:
                raise TypeError
        # If a TypeError is raised, asks user to try again
        except TypeError:
            print(
f"The product code \"{user_input}\" you entered was not ",
"valid. Please ensure that your code is entered as follows and try again:",
'"SKUXXXXX" where X is a number from 0-9.'
)
            continue
        else:
            break
    # Searches the list of shoes for a shoe with that product code
    for shoe in shoe_list:
        # If a match for the product code is found, assigns it to the
        # searched_shoe variable
        if shoe.code == user_input:
            searched_shoe = shoe
    # If no match is found, searched shoe will remain None and so
    # prints an error message and allows the user to try again
    if searched_shoe is None:
        print(f"Sorry, a shoe with the product code {user_input} could \
not be found. Please try again.")
        search_shoe()
    # Otherwise, prints the __str__ information for that shoe
    else:
        print(searched_shoe)


def value_per_item():
    '''
    This function will calculate the total value for each item.
    Please keep the formula for value in mind: value = cost * quantity.
    Print this information on the console for all the shoes.
    '''
    for shoe in shoe_list:
        # Calculates the value per shoe by multiplying the cost and the quantity together.
        value_per_shoe = shoe.get_cost() * shoe.get_quantity()
        # Assigns a new attribute to the shoe with the value per shoe.
        shoe.value_per_item = value_per_shoe
    # Creates an empty list for storing shoe objects as dictionaries.
    shoes_dict_list = []
    # For each shoe in the list, appends the dictionary of an object to the lists.
    for shoe in shoe_list:
        shoes_dict_list.append(shoe.__dict__)
    # Converts the dictionary to a dataframe.
    shoes_dataframe = pandas.DataFrame(shoes_dict_list)
    # Capitalises the first letter of each of the headers.
    shoes_dataframe.columns = map(str.capitalize, shoes_dataframe.columns)
    # Creates a table from the shoes dataframe and prints it.
    table = tabulate.tabulate(shoes_dataframe, headers="keys",
                              tablefmt="fancy_grid")
    print(table)


def highest_qty():
    '''
    Write code to determine the product with the highest quantity and
    print this shoe as being for sale.
    '''
    # Calls the function to find the highest stock
    find_highest_stock()
    # Prints a notice saying the highest quantity shoe is for sale
    print(f"{highest_quantity_product.product}s on sale now!!! Get them fast\
, only {highest_quantity_product.get_quantity()} left in stock!")

#==========Main Menu=============# 
# Menu that executes each function above.
menu_selection = ""
# Displays a menu until the user enters quit
while menu_selection != "q":
    # Prints a list of options for the menu
    menu_selection = input("""\nWelcome to the Nike inventory manager! What would you like to do?\n
rd -  Read data from inventory.txt file and save it to an inventory list
a -   Add a new shoe to the inventory list
v -   View data about every shoe in the inventory list
rs -  Restock the lowest quantity shoe in the inventory list
s -   Search for a shoe by product code
vps - Show the value per shoe (cost*quantity) for each shoe in the inventory list
h -   Print an \'on sale\' notice for the product with the highest quantity
q -   Quit the program
\nEnter your choice: """).lower().replace(" ", "")

    if menu_selection == "rd":
        read_shoes_data()
        print("inventory.txt read and saved to list successfully.")
    
    elif menu_selection == "a":
        capture_shoes()
    
    elif menu_selection == "v":
        view_all()
    
    elif menu_selection == "rs":
        re_stock()
    
    elif menu_selection == "s":
        search_shoe()
    
    elif menu_selection == "vps":
        value_per_item()
   
    elif menu_selection == "h":
        highest_qty()
    
    elif menu_selection == "q":
        print("Thank you for using the Nike inventory manager. Goodbye!")
        quit()

    else:
        print(f"The option {menu_selection} you selected is invalid. Please try again.")
        continue