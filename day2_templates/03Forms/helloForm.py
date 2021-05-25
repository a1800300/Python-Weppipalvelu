from flask import Flask, render_template

app= Flask(__name__)


@app.route('/')
def index():
	return render_template('base.html')


@app.route('/form')
def form():
	return render_template('form.html', methods=['GET','POST'])


@app.route('/foo')
def foo():
	return render_template('foo.html')

@app.route('/pants')
def pants():
	pants = [ "green pants" , "jeans" ]
	return render_template('pants.html', pants=pants)

if __name__ == '__main__':
	app.run()
