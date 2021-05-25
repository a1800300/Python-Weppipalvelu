from flask import Flask, render_template

app= Flask(__name__)


@app.route('/')
def  index():

	hats = ["lippis","pipo"]
	return render_template('loopHTML.html' , hats=hats)


if __name__ == '__main__':
	app.run()
