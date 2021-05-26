from flask import Flask, render_template, request, flash, redirect
#from flask_sqlalchemy import SQLAlchemy
#from flask_wtf import FlaskForm
#from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = 'kahChae4eecohnii1eagoopai2peap'

@app.route('/')
def index():
	return render_template('base.html')

# flash-message1
@app.route('/message-one')
def msgPage():
	flash('This is message one')
	return redirect('/')

# flash-message2
@app.route('/message-two')
def msgPageB():
	flash('This is an another message')
	return redirect('/')


if __name__ == '__main__':
	app.run()
