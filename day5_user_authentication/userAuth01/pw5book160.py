from flask import Flask,render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm #m
from wtforms.ext.sqlalchemy.orm import model_form #m

#users
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, validators

app = Flask(__name__)
db =  SQLAlchemy(app) 
app.secret_key = "ooshouquoh2Ree8Ohphaosai4phoh5"

class Books(db.Model): #m
	id = db.Column(db.Integer, primary_key=True)
	storyline = db.Column(db.Text(160), nullable=False)
	book = db.Column(db.String, nullable=False)

BookForm = model_form(Books, base_class=FlaskForm, db_session=db.session)

# users
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, nullable=False, unique=True)
	passwordHash = db.Column(db.String, nullable=False)

	def setPassword(self, password):
		self.passwordhash = generate_password_hash(self.passwordHash, password)

class UserForm(FlaskForm):
	email = StringField("email", validators=[validators.Email()])
	password = PasswordField("password", validators=[validators.InputRequired()])

# User utility functions

def currentUser():
	try:
		uid = int(session["uid"])
	except:
		return None
	return Users.query.get(id)

app.jinja_env.globals["currentUser"] = currentUser

# User view

@app.route('/user/login', methods=["GET","POST"])
def loginView():
	form = UserForm()

	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data

		user = Users.query.filter_by(email=email).first()
		if not user:
			flash("Login failed.")
			return redirect("/user/login")

		session["uid"] = user.id
		flash("Login ok")
		return redirect("/")

	return render_template("login.html", form=form)


@app.route("/user/register", methods=["GET","POST"])
def registerView():
	form = UserForm()

	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data

		user = Users(email=email)
		user.setPassword(password)
		db.session.add(user)
		sb.session.commit()

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

	book = Books(storyline = "Mermaid goes on adventure and meets Sarah", book="Mermaid meets Sarah")
	db.session.add(book)
	db.session.commit()

@app.route('/', methods =["GET","POST"])
def index():
	stories = Books.query.all()
	return render_template('home.html', stories=stories )

@app.route('/<int:id>/edit', methods =["GET","POST"])
@app.route('/new', methods =["GET","POST"])
def newStory(id=None):
	book = Books()
	if id:
		book = Books.query.get_or_404(id)

	form = BookForm()
	if form.validate_on_submit():
		form.populate_obj(book)
		db.session.add(book)
		db.session.commit()

		flash("Book added!")
		return redirect("/")

	return render_template('new.html', form=form)

@app.route('/home', methods =["GET","POST"])
def home():
	stories =  Books.query.all()
	return render_template('home.html', stories=stories)

@app.route('/<int:id>/delete')
def deleteBook(id):
	book = Books.query.get_or_404(id)
	db.session.delete(book)
	db.session.commit()

	flash("Deleted")
	return redirect("/")

if __name__=="__main__":
	app.run()
