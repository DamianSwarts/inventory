# inventory
# Shoe Inventory Management System

This project is a Python-based Shoe Inventory Management System. It allows users to manage an inventory of shoes, including adding new shoes, viewing all shoes, and capturing shoe data. The system is important for keeping track of shoe inventory and ensuring efficient management of resources.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Credits](#credits)

## Installation
To install the project locally, follow these steps:
1. Clone the repository using the following command:
```
git clone https://github.com/username/ShoeInventoryManagementSystem.git
```
2. Navigate to the project folder.
3. Ensure that Python is installed on your system. If not, download and install Python from [here](https://www.python.org/downloads/).
4. Ensure that the `pandas` and `tabulate` Python libraries are installed. If not, install them using pip:
```
pip install pandas tabulate
```
5. Run the Python script using the command:
```
python main.py
```

## Usage
After installing the project, you can use it as follows:
1. Run the Python script.
2. The script will prompt you to enter details about a shoe, such as the country, code, product, cost, and quantity.
3. After entering the details, the script will create a `Shoe` object and append it to a list of shoes.
4. You can then choose to view all shoes or capture shoe data.
5. The script will read and write data from and to a text file named `inventory.txt`.

Please note that the script is interactive and will guide you through the process.

## Credits
This project was created by [Damian Swarts](https://github.com/DamianSwarts). Contributions are welcome. Please feel free to fork the repository and submit a pull request.
