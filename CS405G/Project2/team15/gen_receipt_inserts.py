import string
import csv

import mysql.connector
from mysql.connector import Error

HOST = "mysql.cs.uky.edu"
USER = "bbri226"
PASSWORD = ""

TEAM15_CUSTOMER_N_BIZ_FILE = "team15_customerAndBiz_table.txt"
TEAM15_RECEIPT_FILE = "team15_receiptsTab_table.txt"
TEAM15_ADDRESS_SCHEMA = [
  "ID", "primaryName", "lastName", "middleInital", "StreetNum", "StreetName",
  "suiteNum", "building", "IsBusiness", "zipCode", "city", "state",
  "telephoneNum"
]
TEAM15_RECEIPT_SCHEMA = [
  "businessName", "numItems", "TotalPrice", "StreetNum", "streetName",
  "BuyDate", "blobPic", "Buyer", "Seller", "City", "State", "zipCode",
  "telephoneNum", "HighestPrice", "LowestPrice"
]
SPECIAL_CASES = {
   "RAY L HYATT301 Hilltop Avenue Room 102, Lexington, KY 40506": 2,
   "RAY L HYATT300 ROSE STREET Hardyman Building Room 102, Lexington, KY 40506": 1,
   "BOB": 7,
   "Stephen Strange": 5,
   "BOWMAN": 8,
   "KROGER": 13,
   "Target": 15,
   "McDonalds": 29
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


#parse their recipt
def parse_team15_receipts(row):
  data = {}
  #load into a list of dict
  for i in range(len(TEAM15_RECEIPT_SCHEMA)):
    if i == 1:
       data[TEAM15_RECEIPT_SCHEMA[i]] = int(row[i].replace('"', ''))
    elif i == 2 or i == 13 or i == 14:
       data[TEAM15_RECEIPT_SCHEMA[i]] = float(row[i].replace('"', ''))
    else:
       data[TEAM15_RECEIPT_SCHEMA[i]] = row[i].replace('"', '')

  return data

#loading team 15 receipts info for testing purposes
def load_receipt_info():
   raw = []
   with open(TEAM15_RECEIPT_FILE , "r") as f:
     raw = f.readlines()
     data = []
     for line in raw:
      if "INSERT" in line:
       continue
      elements = [
       '"{}"'.format(x)
       for x in list(csv.reader([line], delimiter=',', quotechar="'"))[0]
      ]
      data.append(parse_team15_receipts(elements))
   return data

def is_business(row):
  if row[2] == "PORTER" or row[2] == "SYDELL":
      return False
  for i in range(len(TEAM15_ADDRESS_SCHEMA)):
    if TEAM15_ADDRESS_SCHEMA[i] == "IsBusiness":
      if row[i] == "YES" or row[i] == "YEs":
        return True
      else:
        return False

def parse_team15_schema_row(row):
  data = {}
  for i in range(len(TEAM15_ADDRESS_SCHEMA)):
    data[TEAM15_ADDRESS_SCHEMA[i]] = row[i]

  data[TEAM15_ADDRESS_SCHEMA[8]] = is_business(row)

  return data

#get team 15 biz name fun
def get_biz_name(data):
  name = data["primaryName"]
  name = name.replace('"', '')
  if name[len(name) - 1] == " ":
    name = name[:len(name) - 1]

  return name

#get team 15 consumer name func
def get_consumer_name(data):
  primaryName = data["primaryName"]
  middleInitial = data["middleInital"]
  lastName = data["lastName"]
  if "NULL" in middleInitial:
    name = f"{primaryName} {lastName}"
  else:
    name = f"{primaryName} {middleInitial} {lastName}"
  if name[len(name) - 1] == " ":
    name = name[:len(name) - 1]
  return name

# team 15 address func
def get_address(data):
  street_number = data["StreetNum"]
  street_name = data["StreetName"]
  suite_num = data["suiteNum"]
  if "ROOM" in suite_num:
      suite_num = suite_num.strip("ROOM")
  building = data["building"]
  city = data["city"]
  state = data["state"]
  zip = data["zipCode"]
  if suite_num == "NULL" and building == "NULL":
    address = f"{street_number} {street_name}, {city}, {state} {zip}"
  elif suite_num == "NULL":
    address = f"{street_number} {street_name} {building}, {city}, {state} {zip}"
  elif building == "NULL":
    address = f"{street_number} {street_name} Room {suite_num}, {city}, {state} {zip}"
  else:
    address = f"{street_number} {street_name} {building} Room {suite_num}, {city}, {state} {zip}"
  return address

def load_team15_contact_data():
    contact_data = []
    with open(TEAM15_CUSTOMER_N_BIZ_FILE, "r") as f:
        lines = f.readlines()

    for line in lines:
        if "INSERT" in line:
            continue
        elements = [
          '"{}"'.format(x)
          for x in list(csv.reader([line], delimiter=',', quotechar='"'))[0]
        ]
        for i in range(len(elements)):
            elements[i] = elements[i].strip('"').strip("'").replace("'", "")
            if elements[i].endswith(" "):
                elements[i] = elements[i][:len(elements[i]) - 1]
        if len(elements) == 14:
            elements.pop(13)
        data = parse_team15_schema_row(elements)
        if data["IsBusiness"]:
            entity_name = '000000'
            business_name = get_biz_name(data)
        else:
            entity_name = get_consumer_name(data)
            business_name = '000000'
        full_address = get_address(data)
        new_contact = {
           "ID": int(data["ID"]),
           "entity_name": entity_name,
           "business_name": business_name,
           "address": full_address
        }
        contact_data.append(new_contact)

    return contact_data

def get_name_and_addr(ident, team15_contacts):
    for contact in team15_contacts:
        if contact["ID"] == ident:
            return (contact["entity_name"], contact["business_name"], contact["address"])

def get_team11_id(entity_info, team11_contacts):
  for contact in team11_contacts:
     if contact[1] == entity_info[0] and contact[3] == entity_info[2]:
        return contact[0]
     if contact[2] == entity_info[1] and contact[3] == entity_info[2]:
        return contact[0]

def gen_receipt_inserts(receipt, team11_contacts, team15_contacts):
    buyer_id = int(receipt["Buyer"])
    seller_id = int(receipt["Seller"])
    buyer_info = get_name_and_addr(buyer_id, team15_contacts)
    seller_info = get_name_and_addr(seller_id, team15_contacts)
    supplier_id = get_team11_id(seller_info, team11_contacts)
    consumer_id = get_team11_id(buyer_info, team11_contacts)
    if consumer_id is None:
    	for name in SPECIAL_CASES.keys():
    	    if "RAY" in buyer_info[0]:
    	        if (buyer_info[0] + buyer_info[2]) == name:
    	            consumer_id = SPECIAL_CASES[name]
    	    if name in buyer_info[0]:
    	        consumer_id = SPECIAL_CASES[name]
    if supplier_id is None:
    	for name in SPECIAL_CASES.keys():
    	    if "RAY" in seller_info[0]:
    	        if (seller_info[0] + seller_info[2]) == name:
    	            supplier_id = SPECIAL_CASES[name]
    	    if name in seller_info[1]:
    	        supplier_id = SPECIAL_CASES[name]
    if supplier_id is None:
        print(f"Supplier: {seller_info}")
    if consumer_id is None:
        print(f"Consumer: {buyer_info}")
    date = receipt["BuyDate"]
    quantity = receipt["numItems"]
    total_sale = receipt["TotalPrice"]
    highest = receipt["HighestPrice"]
    lowest = receipt["LowestPrice"]
    command = f"INSERT INTO RECEIPT\n\t(supplier_id, consumer_id, date, quantity, total_sale, receipt_image, highest, lowest)\n\tVALUES\n\t({supplier_id}, {consumer_id}, '{date}',\n\t{quantity}, {total_sale}, NULL, {highest}, {lowest});"
    print(command)


connection = create_connection(HOST, USER, PASSWORD, USER)
team11_contact_info = execute_read_query(connection, "SELECT * FROM CONTACT;")
team15_contact_info = load_team15_contact_data()
receipt_data = load_receipt_info()
for receipt in receipt_data:
    gen_receipt_inserts(receipt, team11_contact_info, team15_contact_info)