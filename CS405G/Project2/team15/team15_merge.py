import string
import csv
import mysql.connector
from mysql.connector import Error


TEAM15_CUSTOMER_N_BIZ_FILE = "team15_customerAndBiz_table.txt"
CONTACT_COMMAND_PREFIX = "INSERT INTO CONTACT (entity_name, business_name, address, street_address, city, state, zip, phone_number, duplicate, new) VALUES "
RECEIPT_COMMAND_PREFIX = "INSERT INTO RECEIPT VALUES "
DUPLICATES = []
TEAM15_ADDRESS_SCHEMA = [
  "ID", "primaryName", "lastName", "middleInital", "StreetNum", "StreetName",
  "suiteNum", "building", "IsBusiness", "zipCode", "city", "state",
  "telephoneNum"
]
TEAM15_CNAME_COMPONENTS = ["primaryName", "middleInital", "lastName"]
TEAM15_ADDRESS_COMPONENTS = [
  "StreetNum", "StreetName", "suiteNum", "building", "IsBusiness", "zipCode",
  "city", "state"
]
TEAM15_RECEIPT_SCHEMA = [
  "BuyDate", "numItems", "TotalPrice", "blobPic", "HighestPrice", "LowestPrice"
]

TEAM11_CONTACT_SCHEMA = [
  "id", "entity_name", "business_name", "address", "street_address", "city",
  "state", "zip", "phone_number"
]
TEAM11_RECEIPT_SCHEMA = [
  "id", "supplier_id", "consumer_id", "date", "quantity", "total_sale",
  "receipt_image", "highest", "lowest"
]

SPECIAL_CASES = ["John Wick", "RAY L HYATT", "Tony Stark", "Stephen Strange", "BOB"]
SPECIAL_BUSINESS_CASES = ["EUCLIDE", "500 W New Circle", "500 S Upper", "500 W NEW CIRCLE"]


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

# is biz? Easy for formatting
def is_business(row):
  if row[2] == "PORTER" or row[2] == "SYDELL":
      return False
  for i in range(len(TEAM15_ADDRESS_SCHEMA)):
    if TEAM15_ADDRESS_SCHEMA[i] == "IsBusiness":
      if row[i] == "YES" or row[i] == "YEs":
        return True
      else:
        return False


# *****
def parse_team15_schema_row(row):
  data = {}
  for i in range(len(TEAM15_ADDRESS_SCHEMA)):
    data[TEAM15_ADDRESS_SCHEMA[i]] = row[i]

  data[TEAM15_ADDRESS_SCHEMA[8]] = is_business(row)

  return data


#parse team 15 addr schema row
def parse_team15_addr_schema(row):
  data = {}
  for i in range(len(TEAM15_ADDRESS_SCHEMA)):
    if i == 0:
      data[TEAM15_ADDRESS_SCHEMA[i]] = int(row[i].replace('"', ''))
    elif i == 8:
      if row[i] == "YES":
        data[TEAM15_ADDRESS_SCHEMA[i]] = True
      else:
        data[TEAM15_ADDRESS_SCHEMA[i]] = False
    elif i == 12:
      if len(row[i]) > 10:
        data[TEAM15_ADDRESS_SCHEMA[i]] = str(row[i].replace(".", '')).replace(
          ' ', '')
      else:
        data[TEAM15_ADDRESS_SCHEMA[i]] = str(row[i].replace("-", '')).replace(
          ' ', '')
  return data


#loading team 15 customer n biz info
def load_customer_biz():
  raw = []
  with open(TEAM15_CUSTOMER_N_BIZ_FILE, "r") as f:
    raw = f.readlines()
  data = []
  for line in raw:
    if "INSERT" in line:
      continue
    elements = [
      '"{}"'.format(x)
      for x in list(csv.reader([line], delimiter=',', quotechar="'"))[0]
    ]
    data.append(parse_team15_addr_schema(elements))
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


#check if it matches
def check_if_match(str1, str2):
  table = str.maketrans(dict.fromkeys(string.punctuation))
  tmp1 = str1.translate(table)
  tmp2 = str2.translate(table)
  tmp1 = tmp1.casefold()
  tmp2 = tmp2.casefold()
  tmp1 = tmp1.split(' ')
  tmp2 = tmp2.split(' ')
  #check for match in name
  for wrd in tmp1:
    if wrd not in tmp2 and wrd != "room":
      return False
  for wrd in tmp2:
    if wrd not in tmp1 and wrd != "room":
      return False
  return True


#isDuplicate func
def is_duplicate(contact_data, new_contact):
  new_name = new_contact["entity_name"]
  new_bname = new_contact["business_name"]
  new_addr = new_contact["address"]
  for name in SPECIAL_CASES:
      if name in new_name:
          return True
  if new_name == "000000":
      for case in SPECIAL_BUSINESS_CASES:
          if case in new_addr:
              return True
  for contact in contact_data:
    entity_name = contact[1]
    business_name = contact[2]
    addr = contact[3]
    if check_if_match(entity_name, new_name) and check_if_match(
        addr, new_addr):
      DUPLICATES.append(contact[0])
      return True
    if check_if_match(business_name, new_bname) and check_if_match(
        addr, new_addr):
      DUPLICATES.append(contact[0])
      return True
  return False


#gen contact insert function
def gen_CONTACT_inserts(contact_data):
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
    street_address = full_address.split(',')[0]
    city = data["city"].replace('"', '')
    state = data["state"].replace('"', '')
    zip = data["zipCode"].replace('"', '')
    phone_number = data["telephoneNum"].replace('"', '').replace(' ', '')
    new_contact = {
            "entity_name" : entity_name,
            "business_name" : business_name,
            "address" : full_address
    }
    if (is_duplicate(contact_data, new_contact)):
      continue
    # generate insert command
    if phone_number:
      command = f"{CONTACT_COMMAND_PREFIX} (\n\t'{entity_name}', '{business_name}',\n\t'{full_address}',\n\t'{street_address}', '{city}', '{state}', '{zip}',\n\t'{phone_number}', FALSE, TRUE);"
    else:
      command = f"{CONTACT_COMMAND_PREFIX} (\n\t'{entity_name}', '{business_name}',\n\t'{full_address}',\n\t'{street_address}', '{city}', '{state}', '{zip}',\n\tNULL, FALSE, TRUE);"
    print(command)

connection = create_connection(HOST, USER, PASSWORD, USER)
team11_contact_data = execute_read_query(connection, "SELECT * FROM CONTACT;")
gen_CONTACT_inserts(team11_contact_data)
for dup in DUPLICATES:
  if dup < 75:
    command = f"UPDATE CONTACT SET duplicate = TRUE WHERE id = {dup};"
    print(command)
    command = f"UPDATE CONTACT SET new = TRUE WHERE id = {dup};"
    print(command)