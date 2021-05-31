from flask import Flask,render_template, redirect, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm #m
from wtforms.ext.sqlalchemy.orm import model_form #m

#users
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, validators

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="postgres:///sofia"
db =  SQLAlchemy(app)
app.secret_key = "ooshouquoh2Ree8Ohphaosai4phoh5"

class Recipes(db.Model): #m
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	category = db.Column(db.String, nullable=False)
	level = db.Column(db.String, nullable=True)

RecipeForm = model_form(Recipes, base_class=FlaskForm, db_session=db.session)

# users
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, unique=True, nullable=False)
	passwordHash = db.Column(db.String, nullable=False)

	def setPassword(self, password):
		self.passwordHash = generate_password_hash(password)

	def checkPassword(self, password):
		return check_password_hash(self.passwordHash, password)

class UserForm(FlaskForm):
	email = StringField("email", validators=[validators.Email()])
	password = PasswordField("password", validators=[validators.InputRequired()])

class RegisterForm(UserForm):
	key = StringField("registration key", validators=[validators.InputRequired()])

# User utility functions

def currentUser():
	try:
		uid = int(session["uid"])
	except:
		return None
	return User.query.get(uid) # returns none if uid is not found

app.jinja_env.globals["currentUser"] = currentUser

def loginRequired():
	if not currentUser():
		abort(403)

# User view
@app.route('/user/login', methods=["GET","POST"])
def loginView():
	form = UserForm()

	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data

		user = User.query.filter_by(email=email).first()
		if not user:
			flash("Login failed.")
			return redirect("/user/login")

		if not user.checkPassword(password):
			flash("Bad username or password")
			return redirect("/user/login")

		session["uid"] = user.id
		flash("Login ok")
		return redirect("/")

	return render_template("login.html", form=form)


@app.route("/user/register", methods=["GET","POST"])
def registerView():
	form = RegisterForm()

	if form.validate_on_submit():
		if form.key.data!="sofia":
			flash("Wrong key")
			return redirect("user/register")
		user = User()
		user.email = form.email.data
		user.setPassword(form.password.data)
		db.session.add(user)
		db.session.commit()

		flash("Registration ok, pls login")
		return redirect("/user/login")

	return render_template("register.html", form=form)

@app.route("/user/logout")
def logoutUser():
	session["uid"] = None
	flash("Logget out, see ya!")
	return redirect("/")

# adding testdata
@app.before_first_request
def initDb():
	db.create_all()

	recipe = Recipes(name = "Fish and chips", category="Dinner", level="Easy")
	db.session.add(recipe)

	user = User(email="sofia2@example.com")
	user.setPassword("keLLo123")
	db.session.add(user)
	db.session.commit()

@app.route('/', methods =["GET","POST"])
def index():
	recipes = Recipes.query.all()
	return render_template('home.html', recipes=recipes )

@app.route('/<int:id>/edit', methods =["GET","POST"])
@app.route('/new', methods =["GET","POST"])
def newRecipe(id=None):
	recipe = Recipes()
	if id:
		book = Books.query.get_or_404(id)

	form = RecipeForm()
	if form.validate_on_submit():
		form.populate_obj(recipe)
		db.session.add(recipe)
		db.session.commit()

		flash("Recipe added!")
		return redirect("/")

	return render_template('new.html', form=form)

@app.route('/home', methods =["GET","POST"])
def home():
	recipes =  Recipes.query.all()
	return render_template('home.html', recipes=recipes)

@app.route('/<int:id>/delete')
def deleteRecipe(id):
	recipe = Recipes.query.get_or_404(id)
	db.session.delete(recipe)
	db.session.commit()

	flash("Deleted")
	return redirect("/")

if __name__=="__main__":
	app.run()
