from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from form import AddItem, NewUser, LoginUser
from sqlalchemy import func


app = Flask(__name__)
app.config['SECRET_KEY'] = "gryc43u46ct8t47c74"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy()
db.init_app(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    items = db.relationship('Item', backref='user', lazy=True)
    
class Item(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    category = db.Column(db.String(250))
    link = db.Column(db.String(1000))
    address = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    with app.app_context():
        if current_user.is_authenticated:
            result = db.session.execute(db.select(Item).filter(Item.user_id == current_user.id))
            all_items = list(result.scalars())
        else:
            all_items = []
    return render_template("index.html", items=all_items, logged_in=current_user.is_authenticated)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = AddItem()
    item_name = form.name.data
    item_category = form.name.data
    item_link = form.link.data
    item_img = form.img.data
    if form.validate_on_submit():
        with app.app_context():
            user = User.query.get(current_user.id)
            new_item = Item(name=item_name, category=item_category, link=item_link, address=item_img, user=user)
            db.session.add(new_item)
            db.session.commit()
        flash(f"{item_name} has been added")
    return render_template("add.html", form=form, logged_in=current_user.is_authenticated)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = NewUser()
    if form.validate_on_submit():
        user_name = form.name.data
        user_email = form.email.data
        user_password = generate_password_hash(password=form.password.data, method="scrypt", salt_length=16)
        
        q = db.session.query(User.id).filter(func.lower(User.email) == func.lower(user_email))
        if not db.session.query(q.exists()).scalar():
            with app.app_context():
                new_user = User(email=user_email, password=user_password, name=user_name)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, force=True)
            return redirect(url_for('home'))
        else:
            flash("Email Does Not exist")
            return redirect(url_for('login'))
    return render_template("register.html", form=form, logged_in=current_user.is_authenticated)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginUser()
    if form.validate_on_submit():
        user_email = form.email.data
        user_password = form.password.data
        q = db.session.query(User.id).filter(func.lower(User.email) == func.lower(user_email))
        if db.session.query(q.exists()).scalar():
            with app.app_context():
                email = db.session.execute(db.select(User).where(func.lower(User.email) == func.lower(user_email))).scalar()
                password = email.password
                if check_password_hash(password, user_password):
                    login_user(email, remember=True)
                    return redirect(url_for("home"))
                else:
                    flash("Invalid Password, Please try again")
        else:
            flash("Email does not Exist")
            return redirect(url_for("register"))
    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)