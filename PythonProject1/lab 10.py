import psycopg2

try:
    # Connect to your postgres DB
    conn = psycopg2.connect(
        dbname="my_database",
        user="postgres",
        password="pp2lab10",
        host="localhost",
        port="5432"
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Example query
    cur.execute("SELECT version();")

    # Fetch result
    db_version = cur.fetchone()
    print("Database version:", db_version)

    # Close communication
    cur.close()
    conn.close()

except Exception as e:
    print("Error:", e)
