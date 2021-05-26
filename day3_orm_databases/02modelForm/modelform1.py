from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
db = SQLAlchemy(app)
app.secret_key = "zichaishohz9Phei9oaSooz1aiVahh"

class Countries(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	countryName  = db.Column(db.String, nullable=False)
	population = db.Column(db.Integer, nullable=False)	

# form
CountryForm = model_form(Countries,
	base_class=FlaskForm, db_session=db.session)

@app.before_first_request
def initMe():
	db.create_all()
	# Let's add some test data here
	country =  Countries(countryName='Finland', population='5518000')
	db.session.add(country)
	db.session.commit()

@app.route('/')
def index():
	countries =  Countries.query.all()
	return render_template('loopData.html', countries=countries)

@app.route('/country-form', methods=["GET","POST"])
def addForm():
	form = CountryForm()
	print(request.form) #testing
	return render_template('country-form.html', form=form)


if __name__ == '__main__':
	app.run()
