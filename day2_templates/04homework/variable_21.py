from flask import Flask, render_template

app= Flask(__name__)

@app.route('/')
def index():
	banana = "fruit"
	return render_template('banana.html', banana=banana)

if __name__ == '__main__':
	app.run()
