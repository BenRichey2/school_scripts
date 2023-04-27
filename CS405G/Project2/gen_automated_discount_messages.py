import mysql.connector
from mysql.connector import Error

HOST = "mysql.cs.uky.edu"
USER = "bbri226"
PASSWORD = ""
CONTACT_PREF_DOMAIN = ["ALL", "EMAIL", "TEXT", "DNC", "MAIL", "ROBOCALL","FAX","PHONE"]


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

def gen_email(customer_info, business_info):
    business_name = business_info[2]
    customer_name = customer_info[1]
    # TODO: Make sure this is the correct index for the email field
    email = customer_info[12]
    message = f"EMAIL: {business_name}, {customer_name}; {email}; 25% Coupon Code"
    print(message)


def gen_text(customer_info, business_info):
    business_name = business_info[2]
    customer_name = customer_info[1]
    phone = customer_info[8]
    message = f"TEXT: {business_name},{customer_name}; {phone}; 25% Coupon Code"
    print(message)

def gen_letter(customer_info, business_info):
    business_name = business_info[2]
    customer_name = customer_info[1]
    customer_address = customer_info[3]
    message = f"MAIL: {business_name},{customer_name}; {customer_address}; 25% Coupon Code"
    print(message)

def gen_robocall(customer_info, business_info):
    business_name = business_info[2]
    customer_name = customer_info[1]
    phone = customer_info[8]
    message = f"ROBOCALL: {business_name},{customer_name}; {phone}; 25% Coupon Code"
    print(message)

def gen_fax(customer_info, business_info):
    business_name = business_info[2]
    customer_name = customer_info[1]
    phone = customer_info[8]
    message = f"FAX: {business_name},{customer_name}; {phone}; 25% Coupon Code"
    print(message)

def gen_call(customer_info, business_info):
    business_name = business_info[2]
    customer_name = customer_info[1]
    phone = customer_info[8]
    message = f"PHONE: {business_name},{customer_name}; {phone}; 25% Coupon Code"
    print(message)

def gen_all_messages(customer_info, business_info):
    gen_text(customer_info, business_info)
    gen_robocall(customer_info, business_info)
    gen_email(customer_info, business_info)
    gen_letter(customer_info, business_info)

def gen_appropriate_message(customer_info, business_info, pref):
    if pref == "ALL":
        gen_all_messages(customer_info, business_info)
    elif pref == "EMAIL":
        gen_email(customer_info, business_info)
    elif pref == "TEXT":
        gen_text(customer_info, business_info)
    elif pref == "MAIL":
        gen_letter(customer_info, business_info)
    elif pref == "ROBOCALL":
        gen_robocall(customer_info, business_info)
    elif pref == "FAX":
        gen_fax(customer_info, business_info)
    elif pref == "PHONE":
        gen_call(customer_info, business_info)
    else:
        print("ERROR: Invalid contact preference")
        exit()

def gen_discount_messages(receipt_table, connection):
    for receipt in receipt_table:
        customer_id = receipt[2]
        customer_contact_info = execute_read_query(connection, f"SELECT * FROM CONTACT WHERE id = {customer_id}")
        customer_contact_info = customer_contact_info[0]
        if not customer_contact_info[10]:
            continue
        # TODO: Make sure the element at index 11 is the contact preference
        contact_pref = customer_contact_info[11]
        if "DNC" in contact_pref:
            customer_name = customer_contact_info[1]
            print(f"DNC: {customer_name}")
            continue
        business_id = receipt[1]
        business_contact_info = execute_read_query(connection, f"SELECT * FROM CONTACT WHERE id = {business_id}")
        business_contact_info = business_contact_info[0]
        for pref in CONTACT_PREF_DOMAIN:
            if pref == "ALL":
                if pref in contact_pref and "ROBOCALL" not in contact_pref:
                    gen_appropriate_message(customer_contact_info, business_contact_info, pref)
                    continue
            elif pref == "MAIL":
                if pref in contact_pref and "EMAIL" not in contact_pref:
                    gen_appropriate_message(customer_contact_info, business_contact_info, pref)
            elif pref in contact_pref:
                gen_appropriate_message(customer_contact_info, business_contact_info, pref)

connection = create_connection(HOST, USER, PASSWORD, USER)
QUERY = "SELECT * FROM RECEIPT;"
receipt_table = execute_read_query(connection, QUERY)
gen_discount_messages(receipt_table, connection)
