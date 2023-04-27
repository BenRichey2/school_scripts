import mysql.connector
from mysql.connector import Error

HOST = "mysql.cs.uky.edu"
USER = "bbri226"
PASSWORD = ""


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def gen_duplicate_message(customers):
    customer_name = ""
    street_address = ""
    city = ""
    state = ""
    zip = ""
    for customer in customers:
        customer_name = customer[0]
        street_address = customer[1]
        city = customer[2]
        state = customer[3]
        zip = customer[4]
        message = f"---------------------------------\n{customer_name}\n{street_address}\n{city}, {state}, {zip}\n\n\n----------------------------------\n{customer_name}\nIt is great to meet you again! Your favorite food delivery family is growing, looks like you have already met some of our now expanded family. We want you to know that you will now get the same great service from our newly added drivers!\n\nLooking forward to serving you again!\n---------------------------------\n"
        print(message)

connection = create_connection(HOST, USER, PASSWORD, USER)
QUERY = "SELECT entity_name, street_address, city, state, zip FROM CONTACT WHERE duplicate = TRUE AND entity_name != '000000';"
result = execute_read_query(connection, QUERY)
gen_duplicate_message(result)
