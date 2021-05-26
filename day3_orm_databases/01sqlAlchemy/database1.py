from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class Countries(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	countryName  = db.Column(db.String, nullable=False)
	population = db.Column(db.Integer, nullable=False)	

@app.before_first_request
def initMe():
	db.create_all()
	# Let's add some test data here
	country =  Countries(countryName='Finland', population='5180000')
	db.session.add(country)
	db.session.commit()

@app.route('/')
def index():
	countries =  Countries.query.all()
	return render_template('loopData.html', countries=countries)

if __name__ == '__main__':
	app.run()
