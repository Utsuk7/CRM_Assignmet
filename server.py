from flask import Flask,render_template,jsonify,url_for,request,session,redirect
from pymongo import MongoClient
from datetime import datetime,timedelta

app=Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["CRM"]

# Collections
customers_collection = db["customer"]
orders_collection = db["order"]

# directing to all pages
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/customer_details.html')
def customer_details():
    return render_template('customer_details.html')


@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.json
    new_customer = {
        "name": data['name'],
        "email": data['email'],
        "visits": int(data['visits']),
        "last_visit": datetime.strptime(data['last_visit'], "%Y-%m-%d"),
        "total_spends": float(data['total_spends'])
    }
    result = customers_collection.insert_one(new_customer)
    return jsonify({'message': 'Customer added successfully!', 'id': str(result.inserted_id)}), 201

@app.route('/order_details.html')
def order_details():
    return render_template('order_details.html')

@app.route('/add_order',methods=['POST'])
def add_order():
    data=request.json
    new_order={
        "CustomerID":data['CustomerID'],
        'ProductName':data['ProductName'],
        'Amount':float(data['Amount']),
        'Date':data['Date']
    }
    result=orders_collection.insert_one(new_order)
    return jsonify({'message':'Order added successfully!','id':str(result.inserted_id)}),201


# showing details of customers
@app.route('/get_high_spenders', methods=['GET'])
def get_high_spenders():
    ans = list(customers_collection.find({"total_spends": {"$gt": 10000}}))
    for customer in ans:
        customer['_id'] = str(customer['_id'])  # Convert ObjectId to string for JSON serialization
    return jsonify(ans)

@app.route('/get_high_spenders_and_visits', methods=['GET'])
def get_high_spenders_and_visits():
    ans = list(customers_collection.find({"$and": [{"total_spends": {"$gt": 10000}}, {"visits": {"$lte": 3}}]}))
    for customer in ans:
        customer['_id'] = str(customer['_id'])
    return jsonify(ans)

@app.route('/get_inactive_customers', methods=['GET'])
def get_inactive_customers():
    ans = list(customers_collection.find({"last_visit": {"$lt": datetime.now() - timedelta(days=90)}}))
    for customer in ans:
        customer['_id'] = str(customer['_id'])
    return jsonify(ans)

if(__name__=='__main__'):
    app.secret_key='secretive_key'
    app.run(debug=True)