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
        phone_number VARCHAR(20) NOT NULL
    )
''')
conn.commit()

def insert_from_console():
    name = input("Enter name: ")
    surname = input("Enter surname: ")
    phone_number = input("Enter phone: ")
    cur.execute("SELECT id FROM PhoneBook WHERE name = %s and surname = %s", (name, surname))
    existing = cur.fetchone()
    if existing:
        cur.execute("UPDATE PhoneBook SET phone_number = %s WHERE id = %s", (phone_number, existing[0]))
        conn.commit()
        print("Contact already exist, phone number updated")
    else:
        cur.execute("INSERT INTO PhoneBook (name, surname, phone_number) VALUES (%s, %s, %s)", (name, surname, phone_number))
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
    choice = input("Update by (1)name, (2)surname, (3)phone_number? Enter 1, 2 or 3: ")
    if choice == '1':
        old_name = input("Enter old name: ")
        new_name = input("Enter new name: ")
        cur.execute("UPDATE PhoneBook SET name = %s WHERE name = %s", (new_name, old_name))
    elif choice == '2':
        old_surname = input("Enter old surname: ")
        new_surname = input("Enter new surname: ")
        cur.execute("UPDATE PhoneBook SET surname = %s WHERE surname = %s", (new_surname, old_surname))
    elif choice == '3':
        old_phone_number = input("Enter old phone number: ")
        new_phone_number = input("Enter new phone number: ")
        cur.execute("UPDATE PhoneBook SET phone_number = %s WHERE phone_number = %s", (new_phone_number, old_phone_number))
    else:
        print("Invalid choice.")
        return
    conn.commit()
    print("Contact Data Updated")

def query_data():
    print("1. Query all\n2. Query by name\n3. Query by surname\n4. Query by phone_number")
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
        phone_number = input("Enter phone number: ")
        cur.execute("SELECT * FROM PhoneBook WHERE phone_number = %s", (phone_number,))
    else:
        print("Invalid choice.")
        return
    rows = cur.fetchall()
    for row in rows:
        print(row)

def delete_data():
    print("Delete by (1)name, (2)surname or (3)phone_number")
    choice = input("Enter your choice: ")
    if choice == '1':
        name = input("Enter name to delete: ")
        cur.execute("DELETE FROM PhoneBook WHERE name = %s", (name,))
    elif choice == '2':
        surname = input("Enter surname to delete: ")
        cur.execute("DELETE FROM PhoneBook WHERE surname = %s", (surname,))
    elif choice == '3':
        phone_number = input("Enter phone number to delete: ")
        cur.execute("DELETE FROM PhoneBook WHERE phone_number = %s", (phone_number,))
    else:
        print("Invalid choice.")
        return
    conn.commit()
    print("Contact Deleted")

def insert_from_list():
    data_list = []
    n = int(input("How many users you want to add? "))
    for i in range(n):
        name = input(f"Enter name for user {i+1}: ")
        surname = input(f"Enter surname for user {i+1}: ")
        phone_number = input(f"Enter phone number for user {i+1}: ")
        data_list.append((name, surname, phone_number))

    incorrect_data = []
    for name, surname, phone_number in data_list:
        if not phone_number.isdigit() or len(phone_number) < 7:
            incorrect_data.append((name, surname, phone_number))
        else:
            cur.execute("INSERT INTO PhoneBook (name, surname, phone_number) VALUES (%s, %s, %s)", (name, surname, phone_number))
    conn.commit()

    if incorrect_data:
        print("Incorrect phone numbers found:")
        for data in incorrect_data:
            print(data)
    else:
        print("All contacts inserted")

def query_by_pattern():
    print("Choose query by pattern in (1)name, (2)surname, or (3)phone_number")
    choice = input("Enter your choice: ")
    pattern = input("Enter pattern to search: ")

    if choice == '1':
        cur.execute("SELECT * FROM PhoneBook WHERE name ILIKE %s", ('%' + pattern + '%',))
    elif choice == '2':
        cur.execute("SELECT * FROM PhoneBook WHERE surname ILIKE %s", ('%' + pattern + '%',))
    elif choice == '3':
        cur.execute("SELECT * FROM PhoneBook WHERE phone_number ILIKE %s", ('%' + pattern + '%',))
    else:
        print("Invalid choice.")
        return
    rows = cur.fetchall()
    for row in rows:
        print(row)

def query_with_pagination():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))

    cur.execute("SELECT * FROM PhoneBook ORDER BY id LIMIT %s OFFSET %s", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)

while True:
    print("\nMenu:")
    print("1. Insert data from console")
    print("2. Insert data from CSV file")
    print("3. Insert data from list")
    print("4. Update data")
    print("5. Query data")
    print("6. Query data by pattern")
    print("7. Query data with pagination")
    print("8. Delete data")
    print("9. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        insert_from_console()
    elif choice == '2':
        insert_from_csv()
    elif choice == '3':
        insert_from_list()
    elif choice == '4':
        update_data()
    elif choice == '5':
        query_data()
    elif choice == '6':
        query_by_pattern()
    elif choice == '7':
        query_with_pagination()
    elif choice == '8':
        delete_data()
    elif choice == '9':
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 9.")

cur.close()
conn.close()
