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
    
class Item(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)
    category = db.Column(db.String(250))
    link = db.Column(db.String(1000))
    address = db.Column(db.String(1000))
    
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    with app.app_context():
        result = db.session.execute(db.select(Item).order_by(Item.id))
        all_items = list(result.scalars())
    return render_template("index.html", items=all_items)

@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddItem()
    item_name = form.name.data
    item_category = form.name.data
    item_link = form.link.data
    item_img = form.img.data
    if form.validate_on_submit():
        with app.app_context():
            new_item = Item(name=item_name, link=item_link, category=item_category, address=item_img)
            db.session.add(new_item)
            db.session.commit()
    return render_template("add.html", form=form)
    
if __name__ == "__main__":
    app.run(debug=True)