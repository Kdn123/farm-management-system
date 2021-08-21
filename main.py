from flask import Flask, jsonify, render_template, redirect, request
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase


app = Flask(__name__)

cred = credentials.Certificate("farm.json")
firebase_admin.initialize_app(cred)
store = firestore.client()



Config = {
    'apiKey': "AIzaSyCsgiJQi9yV8CC9BEDSRcxROLwmlPYveEg",
    'authDomain': "farm-92b13.firebaseapp.com",
    'databaseURL': "https://farm-92b13-default-rtdb.firebaseio.com",
    'projectId': "farm-92b13",
    'storageBucket': "farm-92b13.appspot.com",
    'messagingSenderId': "882700738398",
    'appId': "1:882700738398:web:716cf7acf3da228a5bb9cf",
    'measurementId': "G-NLMPWDH3NX"
  }

firebase1 = pyrebase.initialize_app(Config)


@app.route("/", methods=['GET', 'POST'])
def create():
    return render_template("register.html")

@app.route("/userlogin", methods=['GET', 'POST'])
def user():
    return render_template("login.html")

@app.route("/", methods=['GET', 'POST'])
def regis():
    email = request.form['email']
    password = request.form['password']
    auth = firebase1.auth()
    auth.create_user_with_email_and_password(
        email=email, password=password)

    data = {
        'email': email,
        'password': password
    }
    db = firebase1.database()
    # db.child('register').child("userid").set(user1['localId'])
    # result = db.child('users/'+user1['userId']).push(data)

    db.child('registeruser').push(data)
    return render_template("login.html")


@app.route("/login", methods=['GET', 'POST'])
def log():
    auth = firebase1.auth()
    email = request.form.get('uname')
    password = request.form.get('psw')
    auth.sign_in_with_email_and_password(email, password)
    return render_template("index.html")
    #database = firebase.database()
    # data = database.child('registeruser').get(user)
    # data_dict = data.val()
    # dict_values = list(data_dict.values())
    # final_data_dict = dict_values[0]



@app.route("/home")
def index():
    return render_template('index.html')


@app.route("/create", methods=['GET', 'POST'])
def createFarm():
    data = request.get_json()
    #farmDit = {}
    name = request.form.get('nm')
    email = request.form.get('el')
    subject = request.form.get('sub')
    message = request.form.get('msg')

    doc_ref = store.collection(u'farms').document()
    doc_ref.set({
        'name': name,
        'email': email,
        'subject': subject,
        'message': message
    })
    return render_template('index.html')

@app.route("/purchase", methods=['GET', 'POST'])
def createCheckout():
    data = request.get_json()
    #farmDit = {}
    firstname = request.form.get('fname')
    lastname = request.form.get('lname')
    username = request.form.get('uname')
    email = request.form.get('el')
    address = request.form.get('add')
    address2 = request.form.get('add2')
    country = request.form.get('cnt')
    state = request.form.get('st')
    zipcode = request.form.get('zp')
    shippingaddress = request.form.get('sad')
    saveinfo = request.form.get('sav')
    paymentmethod = request.form.get('pm')
    nameoncard = request.form.get('nmc')
    creditcardno = request.form.get('cdn')
    cardcvv = request.form.get('cvv')
    expiry = request.form.get('exp')

    doc_ref = store.collection(u'purchase').document()
    doc_ref.set({
        'firstname': firstname,
        'lastname' : lastname,
        'username' : username,
        'email': email,
        'address': address,
        'address2': address2,
        'country': country,
        'state': state,
        'zipcode': zipcode,
        'shippingaddress': shippingaddress,
        'saveinfo': saveinfo,
        'paymentmethod': paymentmethod,
        'nameoncard': nameoncard,
        'creditcardno': creditcardno,
        'cardcvv': cardcvv,
        'expiry': expiry,

    })
    return render_template('purchase.html')


@app.route("/read", methods = ["GET"])
def readData():
    docs = store.collection(u'farms').stream()

    for doc in docs:
        print(f'{doc.id} => {doc.tp_dict()}')

@app.route("/seed")
def seed():
    return render_template('seed.html')


@app.route("/crop")
def crop():
    return render_template('crop.html')


@app.route("/development")
def development():
    return render_template('development.html')


@app.route("/checkout")
def checkout():
    return render_template('checkout.html')



app.run(debug=True)
