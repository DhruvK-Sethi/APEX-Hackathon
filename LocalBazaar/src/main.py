# Import modules
from flask import Flask, redirect, session,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy, query
from geopy import distance
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from decimal import Decimal
import random
import pandas as pd
import sqlite3

from sqlalchemy.util import NoneType

# DEBUG MODE
# debug = False
debug = True

# set up server and database and config
app = Flask(__name__)
app.secret_key = "siteee" #security reasons, can be any random word
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3' #db file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #makes server sqlite logs less verbose
db = SQLAlchemy(app)

#buyers table
#stores customer/user data
class Buyer(db.Model):
    __tablename__ = 'buyers'
    email = db.Column(db.String(100),unique=True,primary_key=True,nullable=False)
    name = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    latitude = db.Column(db.String(100),nullable=True)
    longitude = db.Column(db.String(100),nullable=True)
    state = db.Column(db.String(100),nullable=False)
    city = db.Column(db.String(100),nullable=False)
    phone = db.Column(db.String(100),nullable=False)
    wishlist = db.Column(db.String(2048),nullable=False)
    notification = db.Column(db.String(4096))
    def __init__(self,email,name,password,latitude,longitude,state,city,phone):
        self.email = email
        self.name = name
        self.phone = phone
        self.password = password
        self.latitude = latitude
        self.longitude = longitude
        self.state = state
        self.city = city
        self.wishlist = ' '
        self.notification= "Welcome to the Website |"

#sellers table
#stores seller/provider data
class Seller(db.Model):
    __tablename__ = 'sellers'
    email = db.Column(db.String(100),unique=True,primary_key=True,nullable=False)
    name = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    latitude = db.Column(db.String(100),nullable=False)
    longitude = db.Column(db.String(100),nullable=False)
    shop_state = db.Column(db.String(100),nullable=False)
    shop_city = db.Column(db.String(100),nullable=False)
    shop_name = db.Column(db.String(100),nullable=False)
    phone = db.Column(db.String(100),nullable=False)
    category = db.Column(db.String(100),nullable=False)
    products = db.relationship('Product',backref='sellers',lazy=True)
    notification = db.Column(db.String(4096))
    item_request = db.Column(db.String(4096))
    views = db.Column(db.Integer)
    def __init__(self,email,name,password,latitude,longitude,shop_state,shop_city,shop_name,phone,category):
        self.email = email
        self.name = name
        self.password = password
        self.latitude = latitude
        self.longitude = longitude
        self.shop_name = shop_name
        self.shop_state = shop_state
        self.shop_city = shop_city
        self.phone = phone
        self.category = category
        self.notification = "Welcome to the Website |"
        self.item_request = ""
        self.views = 0

#products table
#stores products data
#each product linked with a ForeignKey to a shop through it's email
#id is unique and primary key for the table
#identifier is used to distinguish products, but can also be common
class Product(db.Model):
    __tablename__ = 'products'
    id= db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    identifier= db.Column(db.Integer,nullable=False)
    shop = db.Column(db.String(100),db.ForeignKey('sellers.email'),nullable=False)
    name = db.Column(db.String(100),nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100),nullable=False)
    stock = db.Column(db.Integer)
    tags = db.Column(db.String(200))
    category = db.Column(db.String(200))
    description = db.Column(db.String(512))
    stock_over_time = db.Column(db.String(256),nullable=False)
    review = db.Column(db.Float,nullable=False)
    def __init__(self,id,identifier,shop,name,price,stock,tags,description,image):
        self.id = id
        self.shop = shop
        self.name = name
        self.price = price
        self.stock = stock
        self.image = image
        self.tags = tags
        self.category = tags.split(' ')[0]
        self.identifier = identifier
        self.description = description
        self.stock_over_time = ''
        self.review = 0.0

#scores table
#stores product scores data
#references a product's identifier as primary key
class Score(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer,primary_key=True,unique=True,nullable=True)
    score = db.Column(db.Float,nullable=True)
    score_over_time = db.Column(db.String(256),nullable=False)
    def __init__(self,id):
        self.id = id
        self.score = 0
        self.score_over_time = ''

#load sample data from excel sheets into sqlite db
def setupDB():
    # Load the .xlsx files into a pandas DataFrame
    dfProducts = pd.read_excel('LocalBazaar/src/Products Db.xlsx')
    dfSellers = pd.read_excel('LocalBazaar/src/Database.xlsx')
    dfscores = pd.read_excel('LocalBazaar/src/Prediction Db.xlsx')
    dfbuyers = pd.read_excel('LocalBazaar/src/buyers.xlsx')

    # Connect to an SQLite database
    conn = sqlite3.connect('instance/db.sqlite3')
    # conn = sqlite3.connect('../var/main-instance/db.sqlite3')
    # clear existing database values from tables
    cursor = conn.cursor()
    table_names = ['sellers','products','scores','buyers']
    for table_name in table_names:
        cursor.execute(f"DELETE FROM {table_name};")
    conn.commit()


    # Write the DataFrame to the database
    dfProducts.to_sql('products', conn, if_exists='replace', index=False)
    dfSellers.to_sql('sellers', conn, if_exists='replace', index=False)
    dfscores.to_sql('scores', conn, if_exists='replace', index=False)
    dfbuyers.to_sql('buyers', conn, if_exists='replace', index=False)

    # Close the connection to the database
    conn.close()

#calculate distance of user from product
def calcDistance(product):
    user = None
    if session['type'] == 'b':
        user = Buyer.query.filter_by(email=session['email']).first()
    else:
        user = Seller.query.filter_by(email=session['email']).first()
    point1 = (user.latitude,user.longitude)
    shop = Seller.query.filter_by(email=product.shop).first()
    point2 = (shop.latitude,shop.longitude)
    return geodesic(point1,point2).km

@app.route('/login/',methods=["GET","POST"])
def login():
    if request.method == "POST":
        #check login info
        email = request.form["email"]
        password = request.form["password"]
        usr = Buyer.query.filter_by(email=email).first()
        type = 'b'
        if not usr:
            usr = Seller.query.filter_by(email=email).first()
            type = 's'
        if not usr:
            return redirect(url_for('registerBuyer'))
        if(usr.password == password):
            session["name"] = usr.name
            session["email"] = usr.email
            session["type"] = type
            return redirect(url_for('home'))
        else:
            return redirect(url_for('registerBuyer'))
    return render_template('landing.html')

@app.route('/register/buyer')
def registerBuyer():
    if request.method == "POST":
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        state = request.form['state']
        city = request.form['city']
        geolocator = Nominatim(user_agent="geoapi")
        latitude = 0
        longitude = 0
        if request.form['latitude'] == '' or request.form['longitude'] == '':
            loc = geolocator.geocode(city + ", " + state + ", India")
            latitude = loc.latitude
            longitude = loc.longitude
        else:
            latitude = request.form['latitude'].split('°')[0]
            longitude = request.form['longitude'].split('°')[0]
        phone = request.form['phone']
        if Seller.query.filter_by(email=email).first():
            #email already used
            return render_template("sign-in-as-user.html")
        if latitude == "" or longitude == "":
            #location not entered
            return render_template("sign-in-as-user.html")
        if email=="" or name == "" or password == "" or state=="" or city=="" or phone=="":
            #details not entered
            return render_template("sign-in-as-user.html")
        byr = Buyer(email,name,password,latitude,longitude,state,city,phone)
        db.session.add(byr)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("sign-in-as-user.html")

@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/register/seller')
def registerSeller():
    if request.method == "POST":
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        shop_state = request.form['state']
        shop_city = request.form['city']
        geolocator = Nominatim(user_agent="geoapi")
        latitude = 0
        longitude = 0
        if request.form['latitude'] == '' or request.form['longitude'] == '':
            loc = geolocator.geocode(shop_city + ", " + shop_state + ", India")
            latitude = loc.latitude
            longitude = loc.longitude
        else:
            latitude = request.form['latitude'].split('°')[0]
            longitude = request.form['longitude'].split('°')[0]
        shop_name = request.form['shopName']
        shop_category = request.form['category']
        phone = request.form['phone']
        if Buyer.query.filter_by(email=email).first():
            #email already used
            return render_template("sign-in-as-seller.html")
        if latitude == "" or longitude == "":
            #location not entered
            return render_template("sign-in-as-seller.html")
        if email=="" or name == "" or password == "" or shop_name == "" or shop_state == "" or shop_city=="" or phone=="":
            #details not entered
            return render_template("sign-in-as-seller.html")
        sllr = Seller(email,name,password,latitude,longitude,shop_state,shop_city,shop_name,phone,shop_category)
        db.session.add(sllr)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("sign-in-as-seller.html")
if __name__ == "__main__":
    with app.app_context():
        if debug:
            setupDB()
        db.create_all()
        print("----------------- DATABASE CREATED -----------------")
    app.run(debug=debug)

