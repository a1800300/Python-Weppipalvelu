from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
db = SQLAlchemy(app)
app.secret_key = "AGeo3GaB6ahc7iefohy9feiy7thahi"

class Cats(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name  = db.Column(db.String, nullable=False)
	type = db.Column(db.String, nullable=False)	

# form
CatForm = model_form(Cats,
	base_class=FlaskForm, db_session=db.session)

@app.before_first_request
def initMe():
	db.create_all()
	# Let's add some test data here
	cat =  Cats(name='CatsyCat', type='fluffy')
	db.session.add(cat)

	cat = Cats(name='Tony', type='small')
	db.session.add(cat)
	db.session.commit()

@app.route('/')
def index():
	cats =  Cats.query.all()
	return render_template('loop-cats.html', cats=cats)

@app.route('/form', methods=["GET","POST"])
def addForm():
	form = CatForm()
	print(request.form) #testing
	return render_template('form.html', form=form)


if __name__ == '__main__':
	app.run()
