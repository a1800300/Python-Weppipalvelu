from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy #m
from flask_wtf import FlaskForm #m
from wtforms.ext.sqlalchemy.orm import model_form #m

app = Flask(__name__)
app.secret_key="geengoh7ieNgieleiK2Eigh7aidoaz"
db = SQLAlchemy(app)

class Chat(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	message = db.Column(db.Text, nullable=False)

ChatForm = model_form(Chat, base_class=FlaskForm, db_session=db.session) #m

@app.before_first_request
def initChatDb():
	db.create_all()

	# adding test data
	chat = Chat(message="Hey there friend!")
	db.session.add(chat)

	chat = Chat(message="Have a nice day")
	db.session.add(chat)

	# commit adding test data
	db.session.commit()

@app.route('/')
def index():
	chat = Chat.query.all()
	return render_template("messages.html", chat=chat)

#update a row in table
@app.route('/<int:id>/edit', methods=[ "GET" , "POST" ])
@app.route('/chat', methods=[ "GET" , "POST" ])
def newChat(id=None):
	chat = Chat()

	if id:
		chat = Chat.query.get_or_404(id)
	
	form = ChatForm(obj=chat) #m

	if form.validate_on_submit():
		form.populate_obj(chat)

		db.session.add(chat)
		db.session.commit()

		print("New chat message")
		flash("Message added")
		return redirect('/')
	return render_template("chat.html", form=form)

if __name__ == "__main__": #m
	app.run()
