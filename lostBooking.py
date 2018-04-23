from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

app = Flask(__name__)
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='root',
                       port=8889,
                       db='flight_ticket_system',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/login")
def login():
	return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')

# Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	username = request.form['email']
	password = request.form['password']

	cursor = conn.cursor()

	query = 'SELECT * FROM user WHERE email = %s'
	cursor.execute(query, (email))

	data = cursor.fetchone()
	error = None

	if(data):
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO user VALUES(%s, %s)'
		cursor.execute(ins, (email, password))
		conn.commit()
		cursor.close()
		return render_template('login.html')

@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))
	data = cursor.fetchone()
	cursor.close()
	error = None
	if(data):
		session['username'] = username
		return redirect(url_for('home'))
	else:
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)