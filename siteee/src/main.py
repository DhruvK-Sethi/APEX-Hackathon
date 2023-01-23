from flask import Flask, redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy

# set up server and database and config
app = Flask(__name__)
app.secret_key = "siteee" #security reasons, can be any random word
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3' #db file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #makes server sqlite logs less verbose
db = SQLAlchemy(app)

@app.route("/home/")
#home page route
def home():
    return render_template("index.html")

@app.route("/")
#main redirect
def root():
    return redirect(url_for("home"))

if __name__ == "__main__":
    # Uncomment when we start using db
    # with app.app_context():
    #     db.create_all()

    # launch app in production or debug mode
    # Debug mode updates live
    # app.run();
    app.run(debug=True);


