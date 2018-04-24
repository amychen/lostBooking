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
@app.route('/registerAuth/<userType>', methods=['GET', 'POST'])
def registerAuth(userType):
	username = request.form['email']
	password = request.form['password']
	cursor = conn.cursor()

	query = 'SELECT * FROM ' + userType + ' WHERE email = %s'
	cursor.execute(query, (username))

	data = cursor.fetchone()
	error = None

	if(data):
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
	 	ins = 'INSERT INTO ' + userType + ' (email, password) VALUES(%s, %s)'
	 	cursor.execute(ins, (username, password))
	 	conn.commit()
	 	cursor.close()
	return render_template('login.html')

@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	username = request.form['username']
	password = request.form['password']
	userType = request.form['usertype']

	cursor = conn.cursor()
	if (userType == "airline_staff"):
		query = 'SELECT * FROM  airline_staff WHERE username = %s and password = %s'
	else:
		query = 'SELECT * FROM ' + userType + ' WHERE email = %s and password = %s'

	cursor.execute(query, (username, password))
	data = cursor.fetchone()
	cursor.close()
	error = None
	if (data == False):
		error = 'Invalid login. Did you register?'
		return render_template('login.html', error=error)
	else: 
		if (userType == "airline_staff"):
			session['username'] = username
		else:
			session['email'] = username
		return redirect(url_for('home'))
			


@app.route('/home')
def home():
	if (session['email'] != ""):
		username = session['username']
		print(username + "\n");
		return render_template('staff.html')
	else:
		username = session['email']
		cursor = conn.cursor()
		query = 'SELECT * FROM customer WHERE username = %s'
		cursor.execute(query, username)
		data = cursor.fetchone()
		cursor.close()
		if (data):
			return render_template('customer.html')
		else:
			return render_template('agent.html')

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')

app.secret_key = 'b\'e3r\xd7\xf4\xc7g\xd7N\xf5\xefV\xb9\xdf\xed\xf2P%~\t\x8f.X\x91'

if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
