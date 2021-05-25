from flask import Flask, render_template
from random import randrange

app = Flask(__name__)

@app.route('/number')
def index():

	number = randrange(10) 
	numbers = ['2' , '5' , '6' , '9']
	return render_template('number.html', numbers=numbers)

if(__name__)=='__main__':
	app.run()
