from sqlite3 import Cursor
from flask import Flask, abort, request
from about_me import me
from mock_data import catalog 
import json
from config import db
from bson import ObjectId 

app = Flask('funguycollective')

@app.route("/", methods=['GET'])
def home():
    return "This is the home page"

#create an about endpoint and show your name
@app.route("/about")
def about():
    return me["first"] + " " + me["last"]

@app.route("/myaddress")
def address():
    return f'{me["address"]["street"]} {me["address"]["number"]}'

###########################
###########################
###########################
# postman -> test endpoints of rest apis


@app.route("/api/catalog", methods=["GET"])
def get_catalog():
    results = []
    cursor = db.products.find({}) # get all data from the collection

    for prod in cursor:
        prod["id"] = str(prod["_id"])
        results.append(prod)
    
    return json.dumps(catalog)


#post method to create new products
@app.route("/api/catalog", methods=["POST"])
def save_product():
    product = request.get_json()
    db.products.insert_one(product)
    product["_id"] = str(product["_id"])

    return json.dumps(product)


#make an endpoint to send back how many products we have in the catalog
@app.route("/api/catalog/count", methods=["GET"])
def get_count():
    cursor = db.products.find({})
    num_items = 0
    for prod in cursor:
        num_items += 1

    return json.dumps(num_items)#return the value


@app.route("/api/product/<id>", methods=["GET"])
def get_product(id):

    for prod in catalog:
        if prod["_id"] == id:
            return json.dumps(prod)

    return abort(404, "id does not match any product")


# @app.route('/api/catalog/total', methods=['GET'])
@app.get("/api/catalog/total")
def get_total():
    cursor = db.products.find({})
    total = 0
    for prod in cursor:
        total += prod["price"]

    return json.dumps(total)


@app.get("/api/products/<category>")
def products_by_category(category):
    results = []
    category = category.lower()
    for prod in catalog:
        if prod["category"].lower() == category:
            results.append(prod)

    return json.dumps(results)

# get the list of  categories
#get /api/categories
@app.get("/api/categories")
def get_unique_categories():
    cursor = db.products.find({})
    results = []
    for prod in cursor:
        cat = prod["category"]
        if not 'cat' in results:
            results.append(cat)

    return json.dumps(results)



# get the cheapest product
@app.get("/api/product/cheapest")
def get_cheapest_product():
    cursor = db.products.find({})
    solution = cursor[0]
    for prod in cursor:
        if prod["price"] < solution["price"]:
            solution = prod


    solution["_id"] = str(solution["_id"])
    return json.dumps(solution)


@app.get("/api/exercise1")
def get_exe1():
    nums = [123,123,654,124,8865,532,4768,8476,45762,345,-1,234,0,-12,-456,-123,-865,532,4768]
    solution = {}

    # A: find the lowest number
    solution["a"] = 1


    # B: find how many numbers are lowe than 500
    solution["b"] = 1

    # C: sum all the negatives ( -xxxx )
    solution["c"] = 1


    # D: find the sum of numbers except negatives
    solution["d"] = 1


    return json.dumps(solution)


app.run(debug=True)