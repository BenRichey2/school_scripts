import mysql.connector
from mysql.connector import Error
import random

HOST = "mysql.cs.uky.edu"
USER = "bbri226"
PASSWORD = ""
CONTACT_PREF_DOMAIN = ["ALL", "EMAIL", "TEXT", "DNC", "MAIL", "ROBOCALL","FAX","PHONE"]
CONTACT_PREF_PHONE = ["TEXT", "ROBOCALL", "PHONE", "FAX"]
CONTACT_PREF_COMMAND_PREFIX = "UPDATE CONTACT SET "
CONTACT_PREF_PRESETS = {
    "Bob" : "TEXT",
    "John Wick" : "ROBOCALL",
    "Tony Stark" : "EMAILROBOCALL",
    "Stephen Strange" : "MAIL",
    "Ray L. Hyatt" : "DNC"
}


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

def gen_contact_pref_commands(contact_info):
    for contact in contact_info:
        pref = ""
        if contact[1] != "000000":
            for name in CONTACT_PREF_PRESETS.keys():
                if name in contact[1]:
                    pref = CONTACT_PREF_PRESETS[name]
            if pref == "":
                pref = CONTACT_PREF_DOMAIN[random.randint(0, len(CONTACT_PREF_DOMAIN) - 1)]
                if contact[8] == None:
                    while pref in CONTACT_PREF_PHONE:
                        pref = CONTACT_PREF_DOMAIN[random.randint(0, len(CONTACT_PREF_DOMAIN) - 1)]
                if contact[12] == None:
                    while pref == "EMAIL":
                        pref = CONTACT_PREF_DOMAIN[random.randint(0, len(CONTACT_PREF_DOMAIN) - 1)]
            print(CONTACT_PREF_COMMAND_PREFIX + f"contact_preference = \"{pref}\" WHERE id = {contact[0]};")

connection = create_connection(HOST, USER, PASSWORD, USER)
contact_info = execute_read_query(connection, "SELECT * FROM CONTACT;")
gen_contact_pref_commands(contact_info)
