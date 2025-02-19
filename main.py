import mysql.connector as mycon
import json
import jwt
import time
import secrets
from tabulate import tabulate

#Connect to AWS Servers
print("Connecting to AWS Server...")
cob = mycon.connect(user="admin", password="adminpass", host="crud-app.c9ayiokeiq4o.ap-south-1.rds.amazonaws.com", database="crud")
print("Connection Successful!")

#Creates a personal secret key
SECRET_KEY = secrets.token_hex(32)

#loads json file called users.json
def load_json():
    with open("users.json", "r") as file:
        return json.load(file)

def login():
    users = load_json()  
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    if username in users and users[username] == password:
        payload = {
            "username": username,
            "exp": time.time() + 3600 
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        print(f"Login successful! Your token is: {token}")
        return token
    else:
        print("Invalid credentials")
        return None

def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print("Token is valid.")
        return decoded
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token.")
        return None

#create entry for a table
def create():
    tab = cob.cursor()
    itemID = int(input("Enter Item ID: "))
    tab.execute('select id from inventory')
    lis = []
    for i in tab:
        lis.append(i[0])
    if itemID in lis:
        print("This ID already exists")
    else:
        itemName = input("Enter Item Name: ")
        qty = int(input("Enter Quantity: "))
        cost = int(input("Enter Cost: "))
        tab.execute(f"INSERT INTO inventory VALUES ({itemID},'{itemName}', {qty}, {cost})")
        cob.commit()
        print("\nUpdated Successfully!")
        read()

#read all entries in a table
def read():
    tab = cob.cursor()
    tab.execute('SELECT * FROM inventory')
    lis = []
    for i in tab:
        lis.append(list(i))
    print("\n", tabulate(lis, headers=["ID", "Item Name", "Quantity", "Cost in Rupees"]), "\n")

#update an entry in the table
def update():
    tab = cob.cursor()
    read()
    id = int(input("Select Item ID: "))
    tab.execute("select id from inventory")
    lis = []
    for i in tab:
        lis.append(i[0])
    if id not in lis:
        print("This id does not exist")
    else:
        print("What would you like to update?\n1.ID\n2.Item Name\n3.Quantity\n4.Cost")
        choice = int(input("Enter Choice: "))
        if choice == 1:
            newval = int(input("Enter New ID: "))
            tab.execute(f'UPDATE inventory SET id = {newval} where id = {id}')
        if choice == 2:
            newval = input("Enter New Item Name: ")
            tab.execute(f'UPDATE inventory SET item_name = "{newval}" where id = {id}')
        if choice == 3:
            newval = int(input("Enter New Quantity: "))
            tab.execute(f'UPDATE inventory SET qty = {newval} where id = {id}')
        if choice == 4:
            newval = int(input("Enter New Cost: "))
            tab.execute(f'UPDATE inventory SET cost = {newval} where id = {id}')
        else:
            print("Invalid Choice")

        cob.commit()
        read()

#delete an entry from the table
def delete():
    tab = cob.cursor()
    read()
    id = int(input("Select Item ID: "))
    tab.execute("select id from inventory")
    lis = []
    for i in tab:
        lis.append(i[0])
    if id not in lis:
        print("This id does not exist")
    else:
        tab.execute(f"DELETE FROM inventory WHERE id = {id}")
        cob.commit()
        read()

if __name__ == "__main__":
    token = login()
    if token:
        user = verify_token(token) #checks if token is verified
        if user:
            while True:
                action = input("Choose operation:\n1. Create\n2. Read\n3. Update\n4. Delete\n0.Exit\nEnter choice: ") #menu
                if action == "1":
                    create()
                elif action == "2":
                    read()
                elif action == "3":
                    update()
                elif action == "4":
                    delete()
                elif action == "0":
                    break
                else:
                    print("Invalid choice")
        else:
            print("Access denied!")
