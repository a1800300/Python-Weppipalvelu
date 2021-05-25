from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('base.html')

@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/yes')
def yes():
	return render_template('yes.html')

if __name__ == '__main__':
	app.run()
