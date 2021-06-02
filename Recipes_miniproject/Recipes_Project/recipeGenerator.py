from flask import Flask,render_template, redirect, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_wtf import FlaskForm #m
from wtforms.ext.sqlalchemy.orm import model_form #m
import random
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
	instructions = db.Column(db.String, nullable=True)

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
			flash("Wrong username or password, please try again!")
			return redirect("/user/login")

		session["uid"] = user.id
		flash("Login ok, welcome!")
		return redirect("/recipes/home")

	return render_template("login.html", form=form)

@app.route("/user/register", methods=["GET","POST"])
def registerView():
	form = RegisterForm()
	user = User()

	if form.validate_on_submit():
		if form.key.data!="sofia":
			flash("Wrong key")
			return redirect("user/register")
		if User.query.filter_by(email=user.email).first():
			return redirect("/user/register")
			flash("Email is already in use, please try another email.")

		user.email = form.email.data
		user.setPassword(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash("Registration completed, you can now login!")
		return redirect("/user/login")
		
			#user.email = form.email.data

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

	recipe = Recipes(name = "Fish and chips", category="Dinner", level="Easy", instructions="http://www.allrecipes.com/recipe/16580/classic-fish-and-chips/")
	db.session.add(recipe)

#	if not User.query.filter_by(email="sofia@example.com").first():
#		user = User(email="sofia@example.com")
#		user.setPassword("")
#		db.session.add(user)

	db.session.commit()

@app.route('/recipes/home', methods =["GET","POST"])
def homeView():
	loginRequired()
	recipes = Recipes.query.all()
	return render_template('home.html', recipes=recipes )

@app.route('/recipes/<int:id>/edit', methods =["GET","POST"])
@app.route('/recipes/new', methods =["GET","POST"])
def newRecipe(id=None):
	loginRequired()

	if id:
		recipe = Recipes.query.get_or_404(id)
	else:
		recipe = Recipes()
	form = RecipeForm(obj=recipe)

	if form.validate_on_submit():
		form.populate_obj(recipe)
		
		db.session.add(recipe)
		db.session.commit()

		flash("Recipe updated, sounds good!")
		return redirect("/recipes/home")

	return render_template('new.html', form=form)

# landing page
@app.route('/', methods =["GET","POST"])
def home():
	return render_template('index.html')

@app.route('/recipes/<int:id>/delete')
def deleteRecipe(id):
	loginRequired()
	recipe = Recipes.query.get_or_404(id)
	db.session.delete(recipe)
	db.session.commit()

	flash("Recipe deleted")
	return redirect("/recipes/home")

#generator ( not working )
#@app.route('/recipes/generate', methods =["GET","POST"])
#def generateR():
#	loginRequired()
#	query = db.session.query(Recipes)
#	rowCount = int(query.count())
#	recipes = query.offset(int(rowCount*random.random())).first()
#	print(recipes)
#	return("Mo")
#	return render_template("random.html", recipes=recipes)

# error handlers
@app.errorhandler(404)
def custom404(e):
	return render_template("error404.html")

@app.errorhandler(403)
def custom403(e):
	return redirect("/user/login")

@app.errorhandler(500)
def custom500(e):
	return render_template("error500.html")

if __name__=="__main__":
	app.run()
