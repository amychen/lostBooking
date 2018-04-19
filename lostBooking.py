from flask import Flask, render_template, request, session, url_for, redirect
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'flight_ticket_system'
app.config['MYSQL_DATABASE_HOST'] = 'localhost:8889'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL()	
mysql.init_app(app)

@app.route("/")
def home():
	return render_template('index.html')

@app.route("/login")
def login():
	return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')

if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)