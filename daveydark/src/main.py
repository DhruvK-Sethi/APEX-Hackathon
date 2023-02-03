from flask import Flask, redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy

# set up server and database and config
app = Flask(__name__)
app.secret_key = "siteee" #security reasons, can be any random word
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3' #db file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #makes server sqlite logs less verbose
db = SQLAlchemy(app)

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
    def __init__(self,email,name,password,latitude,longitude,state,city,phone):
        self.email = email
        self.name = name
        self.phone = phone
        self.password = password
        self.latitude = latitude
        self.longitude = longitude
        self.state = state
        self.city = city

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
    def __init__(self,email,name,password,latitude,longitude,shop_state,shop_city,shop_name,phone):
        self.email = email
        self.name = name
        self.password = password
        self.latitude = latitude
        self.longitude = longitude
        self.shop_name = shop_name
        self.shop_state = shop_state
        self.shop_city = shop_city
        self.phone = phone

@app.route("/home")
#home page route
def home():
    return render_template('index1.html')

@app.route("/login",methods=["GET", "POST"])
#login page route
def login():
    if request.method == "POST":
        #check login info
        email = request.form["email"]
        password = request.form["password"]
        usr = Buyer.query.filter_by(email=email).first()
        if not usr:
            usr = Seller.query.filter_by(email=email).first()
        if not usr:
            return redirect(url_for('register'))
        if(usr.password == password):
            return redirect(url_for('home'))
        else:
            return redirect(url_for('register'))
    return render_template("login.html")

@app.route("/register",methods=["GET", "POST"])
#register page route
def register():
    if request.method == "POST":
        form = request.form["form_id"]
        if(form == 'buyer'):
            email = request.form['email']
            name = request.form['name']
            password = request.form['password']
            latitude = request.form['latitude']
            longitude = request.form['longitude']
            state = request.form['state']
            city = request.form['city']
            phone = request.form['phone']
            if Seller.query.filter_by(email=email).first():
                #email already used
                return render_template("registeration.html")
            if latitude == "" or longitude == "":
                #location not entered
                return render_template("registeration.html")
            if email=="" or name == "" or password == "" or state=="" or city=="" or phone=="":
                #details not entered
                return render_template("registeration.html")
            byr = Buyer(email,name,password,latitude,longitude,state,city,phone)
            db.session.add(byr)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            #seller form
            email = request.form['email']
            name = request.form['name']
            password = request.form['password']
            latitude = request.form['latitude']
            longitude = request.form['longitude']
            shop_state = request.form['state']
            shop_name = request.form['shopName']
            shop_city = request.form['city']
            phone = request.form['phone']
            if Buyer.query.filter_by(email=email).first():
                #email already used
                return render_template("registeration.html")
            if latitude == "" or longitude == "":
                #location not entered
                return render_template("registeration.html")
            if email=="" or name == "" or password == "" or shop_name == "" or shop_state == "" or shop_city=="" or phone=="":
                #details not entered
                return render_template("registeration.html")
            sllr = Seller(email,name,password,latitude,longitude,shop_state,shop_city,shop_name,phone)
            db.session.add(sllr)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template("registeration.html")

@app.route("/")
#main redirect
def root():
    return redirect(url_for("login"))

if __name__ == "__main__":
    # Uncomment when we start using db
    with app.app_context():
        db.create_all()

    # launch app in production or debug mode
    # Debug mode updates live
    # app.run();
    app.run(debug=True)


