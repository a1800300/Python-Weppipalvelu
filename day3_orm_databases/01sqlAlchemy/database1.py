from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class Countries(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	country  = db.Column(db.String, nullable=False)
	population = db.Column(db.Integer, nullable=False)	

@app.before_first_request
def initMe():
	db.create_all()

@app.route('/')
def index():
	return render_template('base.html')

if __name__ == '__main__':
	app.run()
