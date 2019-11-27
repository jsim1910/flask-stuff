import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

products_db = myclient["products"]

order_management_db = myclient["order_management"]

products = {
    100: {"name":"Americano","price":125},
    200: {"name":"Brewed Coffee","price":110},
    300: {"name":"Cappuccino","price":120},
    400: {"name":"Espresso","price":120},
    500: {"name":"Latte","price":140},
    600: {"name":"Cold Brew","price":200}
}

branches = {
    1: {"name":"Katipunan"},
    2: {"name":"Tomas Morato"},
    3: {"name":"Eastwood"},
    4: {"name":"Tiendesitas"},
    5: {"name":"Arcovia"},
}

def get_products():
    product_list = []

    products_coll = products_db["products"]

    for p in products_coll.find({}):
        product_list.append(p)

    return product_list

def get_product(code):
    products_coll = products_db["products"]

    product = products_coll.find_one({"code":code})

    return product

def get_user(username):
    customers_coll = order_management_db['customers']
    user=customers_coll.find_one({"username":username})
    return user

