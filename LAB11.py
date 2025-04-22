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


cur.execute('''
    CREATE OR REPLACE FUNCTION get_records_by_pattern(pattern VARCHAR)
    RETURNS TABLE(id INT, name VARCHAR, surname VARCHAR, phone VARCHAR) AS $$
    BEGIN
        RETURN QUERY 
        SELECT id, name, surname, phone
        FROM PhoneBook
        WHERE name ILIKE '%' || pattern || '%'
        OR surname ILIKE '%' || pattern || '%'
        OR phone ILIKE '%' || pattern || '%';
    END;
    $$ LANGUAGE plpgsql;
''')
conn.commit()


cur.execute('''
    CREATE OR REPLACE PROCEDURE insert_or_update_user(name VARCHAR, phone VARCHAR)
    AS $$
    BEGIN
        IF EXISTS (SELECT 1 FROM PhoneBook WHERE name = name) THEN
            UPDATE PhoneBook SET phone = phone WHERE name = name;
        ELSE
            INSERT INTO PhoneBook (name, phone) VALUES (name, phone);
        END IF;
    END;
    $$ LANGUAGE plpgsql;
''')
conn.commit()


cur.execute('''
   CREATE OR REPLACE PROCEDURE insert_multiple_users_with_validation(names TEXT[], surnames TEXT[], phones TEXT[])
AS $$
DECLARE
    i INT;
    name VARCHAR;
    surname VARCHAR;
    phone VARCHAR;
    incorrect_data TEXT := '';
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        name := names[i];
        surname := surnames[i];
        phone := phones[i];

        IF phone ~ '^\+?\d{10,15}$' THEN
            INSERT INTO PhoneBook (name, surname, phone) VALUES (name, surname, phone);
        ELSE
            incorrect_data := incorrect_data || 'Invalid phone for ' || name || ' ' || surname || ': ' || phone || CHR(10);
        END IF;
    END LOOP;

    -- If there is any incorrect data, raise a notice with the details
    IF incorrect_data <> '' THEN
        RAISE NOTICE 'Incorrect data: %', incorrect_data;
    END IF;
END;
$$ LANGUAGE plpgsql;
''')
conn.commit()


cur.execute('''
    CREATE OR REPLACE FUNCTION query_data_with_pagination(limit_count INT, offset_count INT)
    RETURNS TABLE(id INT, name VARCHAR, surname VARCHAR, phone VARCHAR) AS $$
    BEGIN
        RETURN QUERY 
        SELECT id, name, surname, phone
        FROM PhoneBook
        LIMIT limit_count OFFSET offset_count;
    END;
    $$ LANGUAGE plpgsql;
''')
conn.commit()


cur.execute('''
    CREATE OR REPLACE PROCEDURE delete_user_by_identifier(identifier VARCHAR)
    AS $$
    BEGIN
        DELETE FROM PhoneBook WHERE name = identifier;

        IF NOT FOUND THEN
            DELETE FROM PhoneBook WHERE phone = identifier;
        END IF;
    END;
    $$ LANGUAGE plpgsql;
''')
conn.commit()


def insert_from_console():
    name = input("Enter name: ")
    surname = input("Enter surname: ")
    phone = input("Enter phone: ")
    cur.execute("INSERT INTO PhoneBook (name, surname, phone) VALUES (%s, %s, %s)", (name, surname, phone))
    conn.commit()
    print("New Contact Inserted")

def insert_from_csv():
    filename = input("Enter CSV file path: ")
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            cur.execute("INSERT INTO PhoneBook (name, surname, phone) VALUES (%s, %s, %s)", (row[0], row[1], row[2]))
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
        cur.execute("DELETE FROM PhoneBook WHERE surname = %s", (surname,))
    elif choice == '3':
        phone = input("Enter phone to delete: ")
        cur.execute("DELETE FROM PhoneBook WHERE phone = %s", (phone,))
    else:
        print("Invalid choice.")
        return
    conn.commit()
    print("Contact Deleted")

def query_with_pagination(limit, offset):
    cur.execute("SELECT * FROM query_data_with_pagination(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def insert_or_update_user(name, phone):
    cur.callproc("insert_or_update_user", (name, phone))
    conn.commit()
    print("User inserted/updated successfully")

def insert_multiple_users(users_data):
    cur.callproc("insert_multiple_users", (users_data,))
    conn.commit()

def delete_user_by_identifier(identifier):
    cur.callproc("delete_user_by_identifier", (identifier,))
    conn.commit()
    print(f"User with identifier {identifier} deleted")


while True:
    print("\nMenu:")
    print("1. Insert data from console")
    print("2. Insert data from CSV file")
    print("3. Update data")
    print("4. Query data")
    print("5. Delete data")
    print("6. Query with pagination")
    print("7. Insert/Update user")
    print("8. Insert multiple users")
    print("9. Delete user by identifier")
    print("10. Exit")
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
        limit = int(input("Enter limit: "))
        offset = int(input("Enter offset: "))
        query_with_pagination(limit, offset)
    elif choice == '7':
        name = input("Enter name: ")
        phone = input("Enter phone: ")
        insert_or_update_user(name, phone)
    elif choice == '8':
        users_data = input("Enter users data as a comma-separated list (name,phone), e.g., 'John,1234567890'").split(',')
        insert_multiple_users(users_data)
    elif choice == '9':
        identifier = input("Enter username or phone to delete: ")
        delete_user_by_identifier(identifier)
    elif choice == '10':
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 10.")

cur.close()
conn.close()
