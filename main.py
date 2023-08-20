from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from form import AddItem

app = Flask(__name__)
app.config['SECRET_KEY'] = "gryc43u46ct8t47c74"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy()
db.init_app(app)
Bootstrap(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add")
def add():
    form = AddItem()
    return render_template("add.html", form=form)
    
if __name__ == "__main__":
    app.run(debug=True)