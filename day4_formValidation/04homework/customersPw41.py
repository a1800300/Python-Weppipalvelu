from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy #m
from flask_wtf import FlaskForm #m
from wtforms.ext.sqlalchemy.orm import model_form #m

app = Flask(__name__)
app.secret_key="oob4eiphieKiQu8eengoojae6tohd2"
db = SQLAlchemy(app)

class Customers(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	company = db.Column(db.String, nullable=False)
	phone = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
	contact_person=db.Column(db.String, nullable=False)

CustomerForm = model_form(Customers, base_class=FlaskForm, db_session=db.session) #m

@app.before_first_request
def initCustDb():
	db.create_all()

	# adding test data
	customer = Customers(company="Yritys Oy", phone="0501232", email="a@mail.fi", contact_person= "Janne Jannela")
	db.session.add(customer)

	customer = Customers(company="Järjestö RY", phone="0345122", email="y@jarjesto.fi", contact_person="Tiina Järjestöläinen")
	db.session.add(customer)

	# commit adding test data
	db.session.commit()

@app.route('/')
def index():
	customer = Customers.query.all()
	return render_template("customers.html", customer=customer)

#update a row in table
@app.route('/<int:id>/edit', methods=[ "GET" , "POST" ])
@app.route('/add-customer', methods=[ "GET" , "POST" ])
def newCustomer(id=None):
	customer = Customers()

	if id:
		customer = Customers.query.get_or_404(id)
	
	form = CustomerForm(obj=customer) #m

	if form.validate_on_submit():
		form.populate_obj(customer)

		db.session.add(customer)
		db.session.commit()

		print("New customer")
		flash("Customer added")
		return redirect("/")
	return render_template("add-customer.html", form=form)

#delete a row in table
@app.route('/<int:id>/delete')
def deleteCustomer(id):
	customer = Customers.query.get_or_404(id)
	db.session.delete(customer)
	db.session.commit()

	flash("Deleted")
	return redirect("/")

if __name__ == "__main__": #m
	app.run()
