import psycopg2
import csv


conn = psycopg2.connect(
    dbname="my_database",
    user="postgres",
    password="pp2lab10",
    host="localhost",
    port="5432"
)

cur = conn.cursor()


cur.execute('''
    CREATE TABLE IF NOT EXISTS PhoneBook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        surname VARCHAR(255) NOT NULL,
        phone VARCHAR(20) NOT NULL
    )
''')
conn.commit()

def insert_from_console():
    name = input("Enter name: ")
    surname = input("Enter surname: ")
    phone = input("Enter phone: ")
    cur.execute("INSERT INTO PhoneBook (name, surname, phone_number) VALUES (%s, %s, %s)", (name, surname, phone))
    conn.commit()
    print("New Contact Inserted")

def insert_from_csv():
    filename = input("Enter CSV file path: ")
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            cur.execute("INSERT INTO PhoneBook (name, surname, phone_number) VALUES (%s, %s, %s)", (row[0], row[1], row[2]))
    conn.commit()
    print("Data from CSV file Inserted")

def update_data():
    choice = input("Update by (1)name, (2)surname, (3)phone? Enter 1, 2 or 3: ")
    if choice == '1':
        old_name = input("Enter old name: ")
        new_name = input("Enter new name: ")
        cur.execute("UPDATE PhoneBook SET name = %s WHERE name = %s", (new_name, old_name))
    elif choice == '2':
        old_surname = input("Enter old surname: ")
        new_surname = input("Enter new surname: ")
        cur.execute("UPDATE PhoneBook SET surname = %s WHERE surname = %s", (new_surname, old_surname))
    elif choice == '3':
        old_phone = input("Enter old phone: ")
        new_phone = input("Enter new phone: ")
        cur.execute("UPDATE PhoneBook SET phone = %s WHERE phone = %s", (new_phone, old_phone))
    else:
        print("Invalid choice.")
        return
    conn.commit()
    print("Contact Data Updated")

def query_data():
    print("1. Query all\n2. Query by name\n3. Query by surname\n4. Query by phone")
    choice = input("Enter your choice: ")
    if choice == '1':
        cur.execute("SELECT * FROM PhoneBook")
    elif choice == '2':
        name = input("Enter username: ")
        cur.execute("SELECT * FROM PhoneBook WHERE name = %s", (name,))
    elif choice == '3':
        surname = input("Enter surname: ")
        cur.execute("SELECT * FROM PhoneBook WHERE surname = %s", (surname,))
    elif choice == '4':
        phone = input("Enter phone: ")
        cur.execute("SELECT * FROM PhoneBook WHERE phone = %s", (phone,))
    else:
        print("Invalid choice.")
        return
    rows = cur.fetchall()
    for row in rows:
        print(row)

def delete_data():
    print("Delete by (1)name, (2)surname or (3)phone")
    choice = input("Enter your choice: ")
    if choice == '1':
        name = input("Enter name to delete: ")
        cur.execute("DELETE FROM PhoneBook WHERE name = %s", (name,))
    elif choice == '2':
        surname = input("Enter surname to delete: ")
        cur.execute("DELETE FROM PhoneBook WHERE phone = %s", (surname,))
    elif choice == '3':
        phone = input("Enter phone to delete: ")
        cur.execute("DELETE FROM PhoneBook WHERE phone = %s", (phone,))
    else:
        print("Invalid choice.")
        return
    conn.commit()
    print("Contact Deleted")

while True:
    print("\nMenu:")
    print("1. Insert data from console")
    print("2. Insert data from CSV file")
    print("3. Update data")
    print("4. Query data")
    print("5. Delete data")
    print("6. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        insert_from_console()
    elif choice == '2':
        insert_from_csv()
    elif choice == '3':
        update_data()
    elif choice == '4':
        query_data()
    elif choice == '5':
        delete_data()
    elif choice == '6':
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 6.")

cur.close()
conn.close()
