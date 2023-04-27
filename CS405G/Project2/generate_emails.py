import mysql.connector
from mysql.connector import Error
from random import randint
import string

HOST = "mysql.cs.uky.edu"
USER = "bbri226"
PASSWORD = ""
CONTACT_PREF_DOMAIN = ["ALL", "EMAIL", "TEXT", "DNC", "MAIL", "ROBOCALL","FAX","PHONE"]
EMAIL_DOMAINS = ["gmail.com", "outlook.com", "uky.edu", "yahoo.com"]


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

def generate_n_random_emails(connection, ids, n):
    for i in range(n):
        idx = randint(0, len(ids) - 1)
        id_val = ids[idx]
        QUERY = f"SELECT entity_name FROM CONTACT WHERE id = {id_val};"
        info = execute_read_query(connection, QUERY)
        user_data = info[0]
        entity_name = user_data[0]
        while entity_name == "000000":
            idx = randint(0, len(ids) - 1)
            id_val = ids[idx]
            QUERY = f"SELECT entity_name FROM CONTACT WHERE id = {id_val};"
            info = execute_read_query(connection, QUERY)
            user_data = info[0]
            entity_name = user_data[0]
        name = entity_name.translate(str.maketrans('', '', string.punctuation))
        name = name.replace(" ", "")
        email_idx = randint(0, len(EMAIL_DOMAINS) - 1)
        email = f"{name}@{EMAIL_DOMAINS[email_idx]}"
        command = f"UPDATE CONTACT SET email = '{email}' WHERE id = {id_val};"
        print(command)
    # generate email for Tony Stark b/c we have to
    email_idx = randint(0, len(EMAIL_DOMAINS) - 1)
    name = "TonyStark"
    id_val = 4
    email = f"{name}@{EMAIL_DOMAINS[email_idx]}"
    command = f"UPDATE CONTACT SET email = '{email}' WHERE id = {id_val};"
    print(command)


connection = create_connection(HOST, USER, PASSWORD, USER)
QUERY = "SELECT id FROM CONTACT;"
print(QUERY)
ids = execute_read_query(connection, QUERY)
ids = [ids[i][0] for i in range(len(ids))]
num_emails = randint(0, len(ids) - 1)
generate_n_random_emails(connection, ids, num_emails)