# Mini Task 1
'''
# 1. Create a dictionary for a product (use real or made-up)
#    Fields: name, price, in_stock (true/false), quantity
# 
# 2. Print each field using f-strings
#
# 3. Create a list of 3 products
#
# 4. Loop through and print each product's name and price
#
# 5. Check: "If product price > 100, print 'expensive', else print 'affordable'"

'''
'''
# Product dictionary
product = {
    "name": "Laptop",
    "price": 1200,
    "in_stock": True,
    "quantity": 5
}

print(f"Product: {product['name']}")
print(f"Price: ${product['price']}")
print(f"In stock: {product['in_stock']}")
print(f"Quantity: {product['quantity']}")

# List of products
products = [
    {"name": "Laptop", "price": 1200},
    {"name": "Mouse", "price": 25},
    {"name": "Keyboard", "price": 75}
]

# Loop and print
for product in products:
    print(f"{product['name']}: ${product['price']}")

    # Conditional check
    if product["price"] > 100:
        print("Expensive")
    else:
        print("Affordable")


def get_total_price(products):
   # calculates the total price of the products
   total = 0

   for product in products:
       total += product["price"]

   return total    


print(f"Total Price: ${get_total_price(products)}")

'''
| Technique          | Used For          |
| ------------------ | ----------------- |
| `for item in list` | Simple list loop  |
| `range(len(list))` | Index-based loop  |
| `enumerate(list)`  | Index + value     |
| `dict.keys()`      | Dictionary keys   |
| `dict.values()`    | Dictionary values |
| `dict.items()`     | Key-value pairs   |

'''

# Mini Task 2

# TASK 1: Write a function that takes a password and returns:
# - True if length >= 8
# - False otherwise

# TASK 2: Write a function that takes a list of tasks and returns only:
# - Tasks that have more than 4 characters

# TASK 3: Write a function that takes price and tax_rate, returns total

# TASK 4: Write a function that takes *args (numbers) and returns average

# Try FIRST before checking answers! ⬇️


def isValid(password):
    if len(password) >= 8:
        return True, len(password)
    else:
        return False, len(password)


passwords = ["HeyMAm", "qwerrtrt", "qwerty", "qwerty65432"]

for passwd in passwords:
    status, length = isValid(passwd)
    print(f"Status: {status}, Length: {length}")


# Tasks:
tasks = ["Reading", "Watching", "Playing TV", "Coding", "Debugging"]


def return_tasks(tasks):
    return [task for task in tasks if len(task) > 4]


# [new_item for item in collection if condition]

print(f"Tasks: {return_tasks(tasks)}")


def calculate_total(price, tax_rate):
    return price + (price * tax_rate)


print(calculate_total(100, 0.18))


def average(*args):
    total = 0

    for x in args:
        total += x

    return total / len(args)


print(average(10, 20, 30))
'''

class Task:
    def __init__(self,title,user_id,completed=False):
        self.title = title
        self.user_id = user_id
        self.completed = completed

    def mark_completed(self):
        self.completed = True
        return f"Task: {self.title} completed !!"

    def mark_incomplete(self):
        self.completed = False
        return f"Task: {self.title} incompleted !!"

    def get_status(self):
        status = "Done" if self.completed else "Pending"
        return f"{self.title}: {status}"   

task1 = Task("Learn Python",user_id=1)     
task2 = Task("Learn Javascript",user_id=2)     

print(task1.get_status())
print(task1.mark_completed())
print(task2.get_status())

file = None
try:
  file = open("data.txt")
  data = file.read()
  print(f"Data: {data}")
except FileNotFoundError:
   print("File Not Found Error !!")
finally:      
   if file:
       file.close() # Always close the file !! 