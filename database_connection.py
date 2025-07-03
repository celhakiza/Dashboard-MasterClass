import mysql.connector
from mysql.connector import Error

host = '65.181.111.169'
database = 'vonsungc_sakila'
user = 'vonsungc_dashboardc'
password = 'training2025'

try:
    connection = mysql.connector.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=3306
    )

    if connection.is_connected():
        print(f"Connected to '{database}'. Type your SQL below.")
        print("Type 'exit' or 'quit' to close the session.\n")

        cursor = connection.cursor()

        while True:
            query = input("mysql> ").strip()
            if query.lower() in ['exit', 'quit']:
                break
            if not query.endswith(";"):
                print("End your query with a semicolon (;)")
                continue
            try:
                cursor.execute(query)
                if cursor.with_rows:
                    rows = cursor.fetchall()
                    for row in rows:
                        print(row)
                    print(f"{cursor.rowcount} rows returned.")
                else:
                    connection.commit()
                    print(f"Query OK. {cursor.rowcount} rows affected.")
            except Error as e:
                print("Query Error:", e)

except Error as e:
    print("Connection Error:", e)

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("Connection closed.")
