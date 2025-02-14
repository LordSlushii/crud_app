import mysql.connector as mycon
from tabulate import tabulate
cob = mycon.connect(user = "root", password = "navijune4", host = "localhost", database = "crud")

def create():
    tab = cob.cursor()
    itemID = int(input("Enter Item ID: "))
    itemName = input("Enter Item Name: ")
    qty = int(input("Enter Quantity: "))
    cost = int(input("Enter Cost: "))
    tab.execute(f"INSERT INTO inventory VALUES ({itemID},'{itemName}', {qty}, {cost})")
    cob.commit()
    print("\nUpdated Successfully!")
    read()


def read():
    tab = cob.cursor()
    tab.execute('SELECT * FROM inventory')
    lis = []
    for i in tab:
        lis.append(list(i))
    print("\n",tabulate(lis, headers=["ID","Item Name", "Quantity", "Cost in Rupees"]), "\n")

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
    
    
delete()
