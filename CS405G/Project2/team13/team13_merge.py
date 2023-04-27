import csv
import string
import random

DUPLICATES = []
TEAM13_RECEIPT_FILE = "team13_receipt_table.txt"
SALE_FILE = "team13_sale_table.txt"
ADDRESS_FILE = "team13_address_table.txt"
TEAM11_RECEIPT_FILE = "team11_receipt_table.txt"
TEAM11_CONTACT_FILE = "team11_contact_table.txt"
CONTACT_COMMAND_PREFIX = "INSERT INTO CONTACT (entity_name, business_name, address, street_address, city, state, zip, phone_number) VALUES "
RECEIPT_COMMAND_PREFIX = "INSERT INTO RECEIPT (supplier_id, consumer_id, date, quantity, total_sale, receipt_image, highest, lowest) VALUES "
CONTACT_PREF_COMMAND_PREFIX = "UPDATE CONTACT SET "
CONTACT_PREF_DOMAIN = ["ALL", "EMAIL", "TEXT", "DNC", "MAIL", "ROBOCALL","FAX","PHONE"]
CONTACT_PREF_PHONE = ["TEXT", "ROBOCALL", "PHONE"]
CONTACT_PREF_PRESETS = {
    "Bob" : "TEXT",
    "John Wick" : "ROBOCALL",
    "Tony Stark" : "EMAILROBOCALL",
    "Stephen Strange" : "MAIL",
    "Ray L. Hyatt" : "DNC"
}
TEAM13_ADDRESS_SCHEMA = [
    "id",
    "is_business",
    "name_prefix",
    "first_name",
    "middle_initial",
    "last_name",
    "name_suffix",
    "company_name",
    "street_address",
    "unit_number",
    "city",
    "state",
    "zip_code",
    "phone_number"
]
TEAM13_CNAME_COMPONENTS = [
    "name_prefix",
    "first_name",
    "middle_initial",
    "last_name",
    "name_suffix"
]
TEAM13_ADDRESS_COMPONENTS = [
    "street_address",
    "unit_number",
    "city",
    "state",
    "zip_code"
]
TEAM13_RECEIPT_SCHEMA = [
    "receipt_number",
    "receipt_data",
    "customer_id",
    "company_name",
    "address",
    "receipt_scan"
]
TEAM13_SALE_SCHEMA = [
    "sale_id",
    "receipt_number",
    "items_sold",
    "total_sale",
    "highest_price",
    "lowest_price"
]
TEAM11_CONTACT_SCHEMA = [
    "id",
    "entity_name",
    "business_name",
    "address",
    "street_address",
    "city",
    "state",
    "zip",
    "phone_number"
]
TEAM11_RECEIPT_SCHEMA = [
    "id",
    "supplier_id",
    "consumer_id",
    "date",
    "quantity",
    "total_sale",
    "receipt_image",
    "highest",
    "lowest"
]
SPECIAL_CASES = {
    "704 Euclid Avenue Lexington Kentucky 40502" : 13,
    "345 South Limestone Lexington Kentucky 40508" : 24
}

def is_business(row):
    for i in range(len(TEAM13_ADDRESS_SCHEMA)):
        if TEAM13_ADDRESS_SCHEMA[i] == "is_business":
            if row[i] == '"_binary \"\\0\""':
                return False
            else:
                return True

def parse_team13_schema_row(row):
    data = {}
    data[TEAM13_ADDRESS_SCHEMA[1]] = is_business(row)
    for i in range(2, len(TEAM13_ADDRESS_SCHEMA)):
        data[TEAM13_ADDRESS_SCHEMA[i]] = row[i]

    return data

def parse_team13_sale_schema_row(row):
    data = {}
    for i in range(len(TEAM13_SALE_SCHEMA)):
        if i < 3:
            data[TEAM13_SALE_SCHEMA[i]] = int(row[i].replace('"', ''))
        else:
            data[TEAM13_SALE_SCHEMA[i]] = float(row[i].replace('"', ''))

    return data

def parse_team13_receipt_schema_row(row):
    data = {}
    for i in range(len(TEAM13_RECEIPT_SCHEMA)):
        if i == 0 or i == 2:
            data[TEAM13_RECEIPT_SCHEMA[i]] = int(row[i].replace('"', ''))
        elif i == 5:
            data[TEAM13_RECEIPT_SCHEMA[i]] = row[i].replace('"', '').replace(' ', '')
        else:
            data[TEAM13_RECEIPT_SCHEMA[i]] = row[i].replace('"', '').replace("’", "\'")

    return data

def parse_team13_addr_schema_row(row):
    data = {}
    for i in range(len(TEAM13_ADDRESS_SCHEMA)):
        if i == 0 or i == 12:
            data[TEAM13_ADDRESS_SCHEMA[i]] = int(row[i].replace('"', ''))
        elif i == 1:
            if row[i] == '"_binary \"\\0\""':
                data[TEAM13_ADDRESS_SCHEMA[i]] = False
            else:
                data[TEAM13_ADDRESS_SCHEMA[i]] = True
        else:
            if TEAM13_ADDRESS_SCHEMA[i] == "phone_number":
                data[TEAM13_ADDRESS_SCHEMA[i]] = row[i].replace('"', '').replace(' ', '')
            else:
                data[TEAM13_ADDRESS_SCHEMA[i]] = row[i].replace('"', '')

    return data

def parse_team11_schema_row(row):
    data = {}
    for i in range(len(TEAM11_CONTACT_SCHEMA)):
        if i == 0:
            data[TEAM11_CONTACT_SCHEMA[i]] = int(row[i].replace('"', ''))
        else:
            data[TEAM11_CONTACT_SCHEMA[i]] = row[i].replace('"', '')

    return data

def get_consumer_name(data):
    name = ""
    for part in TEAM13_CNAME_COMPONENTS:
        if part == "name_suffix":
            name += data[part].replace('"', '')
        else:
            name += data[part].replace('"', '') + " "

    name = name.replace("’", "\'")
    name = name.replace("NULL ", "")
    name = name.replace("NULL", "")
    if name[len(name) - 1] == " ":
        name = name[:len(name) - 1]
    return name

def get_business_name(data):
    name = data["company_name"]
    name = name.replace("’", "\'")
    name = name.replace('"', '')
    if name[len(name) - 1] == " ":
        name = name[:len(name) - 1]
    return name

def get_address(data):
    address = ""
    for part in TEAM13_ADDRESS_COMPONENTS:
        if data[part] == '"NULL"' or data[part] == 'NULL':
            continue
        if part == "unit_number":
            address = address[:len(address) - 2]
            address += " Room " + data[part]
        else:
            address += str(data[part])
        if part == "zip_code":
            continue
        if part == "state":
            address += " "
            continue
        address += ", "

    address = address.replace('"', '')
    return address

def check_match(string1, string2):
    table = str.maketrans(dict.fromkeys(string.punctuation))
    tmp1 = string1.translate(table)
    tmp2 = string2.translate(table)
    tmp1 = tmp1.casefold()
    tmp2 = tmp2.casefold()
    tmp1 = tmp1.split(' ')
    tmp2 = tmp2.split(' ')
    # Check for matching words in name
    for ele in tmp1:
        if ele not in tmp2 and ele != "room":
            return False
    for ele in tmp2:
        if ele not in tmp1 and ele != "room":
            return False

    return True

def is_duplicate(contact_data, new_contact):
    new_name = new_contact["entity_name"]
    new_bname = new_contact["business_name"]
    new_addr = new_contact["address"]
    for contact in contact_data:
        entity_name = contact["entity_name"]
        business_name = contact["business_name"]
        addr = contact["address"]
        if check_match(entity_name, new_name) and check_match(addr, new_addr):
            DUPLICATES.append(contact["id"])
            return True
        if check_match(business_name, new_bname) and check_match(addr, new_addr):
            DUPLICATES.append(contact["id"])
            return True

    return False

def gen_CONTACT_inserts(contact_data):
    with open(ADDRESS_FILE, "r") as f:
        lines = f.readlines()

    id_num = contact_data[len(contact_data) - 1]["id"]
    for line in lines:
        if "INSERT" in line:
            continue
        elements = [ '"{}"'.format(x) for x in list(csv.reader([line],
                                                               delimiter=',',
                                                               quotechar='"'))[0]
                                                               ]
        data = parse_team13_schema_row(elements)
        if data["is_business"]:
            entity_name = "000000"
            business_name = get_business_name(data)
        else:
            entity_name = get_consumer_name(data)
            business_name = "000000"
        full_address = get_address(data)
        street_address = data["street_address"].replace('"', '')
        if data["unit_number"] != '"NULL"':
            street_address += " Room " + data["unit_number"].replace('"', '')
        city = data["city"].replace('"', '')
        state = data["state"].replace('"', '')
        zip = data["zip_code"].replace('"', '')
        phone_number = data["phone_number"].replace('"', '').replace(' ', '')
        new_contact = {"id": id_num,
                             "entity_name": entity_name,
                             "business_name": business_name,
                             "address": full_address,
                             "street_address": street_address,
                             "city": city,
                             "state": state,
                             "zip": zip,
                             "phone_number": phone_number}
        if (is_duplicate(contact_data, new_contact)):
            continue
        id_num += 1
        new_contact["id"] = id_num
        contact_data.append(new_contact)
        # generate insert command
        if phone_number != 'NULL':
            command = f"{CONTACT_COMMAND_PREFIX} (\n\t'{entity_name}', '{business_name}',\n\t'{full_address}',\n\t'{street_address}', '{city}', '{state}', '{zip}',\n\t'{phone_number}');"
        else:
            command = f"{CONTACT_COMMAND_PREFIX} (\n\t'{entity_name}', '{business_name}',\n\t'{full_address}',\n\t'{street_address}', '{city}', '{state}', '{zip}',\n\t{phone_number});"
        print(command)

    return contact_data

def load_CONTACT_data():
    raw = []
    with open(TEAM11_CONTACT_FILE, "r") as f:
        raw = f.readlines()
    data = []
    for line in raw:
        if "INSERT" in line:
            continue
        elements = [ '"{}"'.format(x) for x in list(csv.reader([line],
                                                               delimiter=',',
                                                               quotechar="'"))[0]
                                                               ]
        data.append(parse_team11_schema_row(elements))

    return data

def load_team13_sale_data():
    raw = []
    with open(SALE_FILE, "r") as f:
        raw = f.readlines()
    data = []
    for line in raw:
        if "INSERT" in line:
            continue
        elements = [ '"{}"'.format(x) for x in list(csv.reader([line],
                                                               delimiter=',',
                                                               quotechar="'"))[0]
                                                               ]
        data.append(parse_team13_sale_schema_row(elements))

    return data

def load_team13_address_data():
    raw = []
    with open(ADDRESS_FILE, "r") as f:
        raw = f.readlines()
    data = []
    for line in raw:
        if "INSERT" in line:
            continue
        elements = [ '"{}"'.format(x) for x in list(csv.reader([line],
                                                               delimiter=',',
                                                               quotechar='"'))[0]
                                                               ]
        data.append(parse_team13_addr_schema_row(elements))

    return data

def load_team13_receipt_data():
    raw = []
    with open(TEAM13_RECEIPT_FILE, "r") as f:
        raw = f.readlines()
    data = []
    for line in raw:
        if "INSERT" in line:
            continue
        elements = [ '"{}"'.format(x) for x in list(csv.reader([line],
                                                               delimiter=',',
                                                               quotechar="'"))[0]
                                                               ]
        data.append(parse_team13_receipt_schema_row(elements))

    return data

def reconstruct_addr(team13_addr_data, company_name):
    for row in team13_addr_data:
        if row["company_name"] == company_name:
            return get_address(row)
    print("ADDR ERR")


def get_supplier_id(CONTACT_data, team13_addr_data, team13_receipt_data, receipt_num):
    company_name = team13_receipt_data[receipt_num - 1]["company_name"]
    company_addr = team13_receipt_data[receipt_num - 1]["address"]
    if company_addr in SPECIAL_CASES.keys():
        return SPECIAL_CASES[company_addr]
    company_addr = company_addr[:len(company_addr) - 6]
    for row in CONTACT_data:
        if row["business_name"] == company_name and (row["address"])[:len(row["address"]) - 6].replace(",", "").replace(" Room", "") == company_addr:
            return row["id"]

    print("SUPP ERROR")

def get_consumer_id(CONTACT_data, team13_address_data, team13_receipt_data, receipt_num):
    customer_id = team13_receipt_data[receipt_num - 1]["customer_id"]
    customer_name = ""
    customer_addr = ""
    for row in team13_address_data:
        if row["id"] == customer_id:
            customer_name = get_consumer_name(row)
            customer_addr = get_address(row)
    if customer_name == "" or customer_addr == "":
        print("ERROR")
    for row in CONTACT_data:
        if row["entity_name"] == customer_name and row["address"] == customer_addr:
            return row["id"]

    print("CONS ERROR")


def gen_RECEIPT_inserts(CONTACT_data, team13_address_data, team13_receipt_data):
    for sale in team13_sale_data:
        supp_id = get_supplier_id(CONTACT_data, team13_address_data,
                                  team13_receipt_data, sale["receipt_number"])
        cons_id = get_consumer_id(CONTACT_data, team13_address_data,
                                  team13_receipt_data, sale["receipt_number"])
        date = team13_receipt_data[sale["receipt_number"] - 1]["receipt_data"]
        quantity = sale["items_sold"]
        total_sale = sale["total_sale"]
        highest = sale["highest_price"]
        lowest = sale["lowest_price"]
        command = f"{RECEIPT_COMMAND_PREFIX}({supp_id}, {cons_id}, '{date}', {quantity}, {total_sale}, NULL, {highest}, {lowest});"
        print(command)

def gen_UPDATE_commands(old_contact_ids, CONTACT_data):
    dup_commands = []
    new_commands = []
    contact_pref_commands = []
    for contact in CONTACT_data:
        if contact["id"] in DUPLICATES:
            duplicate = "TRUE"
        else:
            duplicate = "FALSE"
        if contact["id"] in old_contact_ids and duplicate == "FALSE":
            new = "FALSE"
        else:
            new = "TRUE"
        dup_commands.append(f"UPDATE CONTACT SET duplicate = {duplicate} WHERE id = {contact['id']};")
        new_commands.append(f"UPDATE CONTACT SET new = {new} WHERE id = {contact['id']};")
        pref = ""
        if contact["entity_name"] != "000000":
            for name in CONTACT_PREF_PRESETS.keys():
                if name in contact["entity_name"]:
                    pref = CONTACT_PREF_PRESETS[name]
            if pref == "":
                pref = CONTACT_PREF_DOMAIN[random.randint(0, len(CONTACT_PREF_DOMAIN) - 1)]
                if contact["phone_number"] == "NULL":
                    while pref in CONTACT_PREF_PHONE:
                        pref = CONTACT_PREF_DOMAIN[random.randint(0, len(CONTACT_PREF_DOMAIN) - 1)]
            contact_pref_commands.append(CONTACT_PREF_COMMAND_PREFIX + f"contact_preference = \"{pref}\" WHERE id = {contact['id']}")
    for command in dup_commands:
        print(command)
    for command in new_commands:
        print(command)
    for command in contact_pref_commands:
        print(command)

if __name__ == "__main__":
    team11_contact_data = load_CONTACT_data()
    old_contact_ids = [team11_contact_data[i]["id"] for i in range(len(team11_contact_data))]
    new_contact_data = gen_CONTACT_inserts(team11_contact_data)
    team13_sale_data = load_team13_sale_data()
    team13_receipt_data = load_team13_receipt_data()
    team13_addr_data = load_team13_address_data()
    gen_RECEIPT_inserts(team11_contact_data, team13_addr_data, team13_receipt_data)
    gen_UPDATE_commands(old_contact_ids, new_contact_data)
