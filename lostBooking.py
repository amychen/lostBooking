from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors, hashlib, random
from datetime import date
from dateutil.relativedelta import relativedelta
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.charts import Donut, show
import pandas as pd
import numpy as np

app = Flask(__name__)
conn = pymysql.connect(host='localhost',
											 user='root',
											 password='root',
											 port=8889,
											 db='flight_ticket_system',
											 charset='utf8mb4',
											 cursorclass=pymysql.cursors.DictCursor)

cursor = conn.cursor()

@app.route("/login")
def login():
	return render_template('login.html')

@app.route("/register")
def register():
	return render_template('register.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
	return render_template('indexLoggedIn.html')

@app.route("/")
def index():
	try:

		username = session['username']

		user = session['type']
		curr_date = date.today()
		one_month = date.today() + relativedelta(months=+1)
		one_year = date.today() + relativedelta(years=+1)

		if (user == "airline_staff"):
			airline = your_airline()
			try:
				start_date = request.args['start_date']
				end_date = request.args['end_date']
				dpt_airport = request.args['dpt_airport']
				arr_airport = request.args['arr_airport']

				cursor.execute('SELECT * FROM flight WHERE departure_time BETWEEN %s AND %s AND airline_name = %s \
									AND departure_airport=%s AND arrival_airport=%s', (start_date, end_date, airline, dpt_airport, arr_airport))
				
			except Exception as e:
				cursor.execute('SELECT * FROM flight WHERE departure_time BETWEEN %s AND %s AND airline_name = %s', \
											(curr_date, one_month, airline))
				
			flights = cursor.fetchall()

			past_three_month = date.today() + relativedelta(months=-3)
			cursor.execute('SELECT *, count(booking_agent_id) as cnt FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket WHERE \
											purchase_date BETWEEN %s AND %s AND airline_name=%s GROUP BY email, password, booking_agent_id ORDER BY \
											cnt DESC LIMIT 5', (past_three_month, curr_date, airline))
			three_month_agents = cursor.fetchall()
		
			past_year = date.today() + relativedelta(years=-1)
			cursor.execute('SELECT *, count(booking_agent_id) as cnt FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket \
											WHERE purchase_date BETWEEN %s AND %s AND airline_name=%s GROUP BY email, password, booking_agent_id ORDER BY \
											cnt DESC LIMIT 5', (past_year, curr_date, airline))
			past_year_agents = cursor.fetchall()

			cursor.execute('SELECT email, booking_agent_id, sum(price*0.2) as commission FROM booking_agent NATURAL JOIN \
											purchases NATURAL JOIN flight NATURAL JOIN ticket WHERE purchase_date BETWEEN %s AND %s AND airline_name=%s \
											GROUP BY email, password, booking_agent_id ORDER BY commission DESC LIMIT 5', (past_year, curr_date, airline))
			commission_past_year_agent = cursor.fetchall()

			top_customer = frequent_customer()['customer_email']
			purchase_ticket = frequent_customer()['purchase_num']

			months_ticket = [0]*12
			months = []
			total = 0

			try: 
				report_start_date = request.args['report_start_date']
				report_end_date = request.args['report_end_date']
				cursor.execute('SELECT purchase_date FROM purchases NATURAL JOIN ticket WHERE purchase_date BETWEEN %s AND %s AND \
												airline_name=%s', (report_start_date, report_end_date, airline))
			except:
				cursor.execute('SELECT purchase_date FROM purchases NATURAL JOIN ticket WHERE airline_name=%s', airline)

			ticket_date = cursor.fetchall()

			for ticket in ticket_date:
				months.append(int(str(ticket['purchase_date']).split('-')[1]))
				total += 1
			for month in months:
				months_ticket[month - 1] += 1

			months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", \
								"November", "December"]
			
			year_first_day = date(date.today().year, 1, 1)
			year_last_day = date(date.today().year, 12, 31)
			pie_chart = create_pie_chart(year_first_day, year_last_day)

			script, div = components(pie_chart[0])
			cust_revenue_year = pie_chart[1]
			agent_revenue_year = pie_chart[2]

			pie_chart = create_pie_chart(year_first_day, year_last_day)
			script, div = components(pie_chart[0])
			cust_revenue = pie_chart[1]
			agent_revenue = pie_chart[2]

			ticket_by_month = create_ticket_by_month(months_ticket, total)
			script1, div1 = components(ticket_by_month)

			cursor.execute('SELECT airport_city, count(arrival_airport) as cnt FROM purchases NATURAL JOIN \
											ticket NATURAL JOIN flight JOIN airport WHERE airport_name = arrival_airport AND purchase_date BETWEEN \
											%s AND %s AND airline_name=%s GROUP BY arrival_airport ORDER BY cnt DESC LIMIT 3', \
											(past_three_month, curr_date, airline))
			top_destination_month = cursor.fetchall()

			cursor.execute('SELECT airport_city, count(arrival_airport) as cnt FROM purchases NATURAL JOIN \
											ticket NATURAL JOIN flight JOIN airport WHERE airport_name = arrival_airport AND purchase_date BETWEEN \
											%s AND %s AND airline_name=%s GROUP BY arrival_airport ORDER BY cnt DESC LIMIT 3', (past_year, curr_date, airline))
			top_destination_year = cursor.fetchall()

			try:
				message = request.args['message']
				return render_template("airline_staff.html", flights=flights, three_month_agents=three_month_agents, past_year_agents = past_year_agents, \
																username=username, airline=airline, message=message, div=div, script=script, div1=div1, \
																script1=script1, agent_revenue_year=agent_revenue_year, cust_revenue_year=cust_revenue_year, \
																top_customer=top_customer, purchase_ticket=purchase_ticket, total=total, \
																top_destination_month=top_destination_month, top_destination_year=top_destination_year, \
																commission_past_year_agent=commission_past_year_agent)
			except:
				return render_template("airline_staff.html", flights=flights, three_month_agents=three_month_agents, past_year_agents=past_year_agents, \
																username=username, airline=airline, div=div, script=script, div1=div1, script1=script1, \
																agent_revenue_year=agent_revenue, cust_revenue_year=cust_revenue, top_customer=top_customer, \
																purchase_ticket=purchase_ticket, total=total, top_destination_month=top_destination_month, \
																top_destination_year=top_destination_year, commission_past_year_agent=commission_past_year_agent)
		elif (user == "booking_agent"):

			cursor.execute('SELECT booking_agent_id FROM booking_agent WHERE email=%s', username)
			idnum = cursor.fetchone()["booking_agent_id"]
			return render_template("booking_agent.html", username=username, idnum=idnum)
		else:
			return render_template("customer.html", username=username)
	except Exception as e:
		print(e)
		return render_template('index.html')

@app.route('/registerAuth/<userType>', methods=['GET', 'POST'])
def registerAuth(userType):
	username = request.form['email']
	password = request.form['password']
	password = calc_md5(password)

	if (userType != "airline_staff"):
		query = 'SELECT * FROM ' + userType + ' WHERE email = %s'
	else:
		query = 'SELECT * FROM ' + userType + ' WHERE username = %s'

	cursor.execute(query, username)
	data = cursor.fetchone()
	error = None
	
	if (data):
		error = "This user already exists"
		return render_template('register.html', error=error)
	else:
		if userType == "customer":
			name = request.form['name']
			buildingNo = request.form['buildingNo']
			street = request.form['street']
			city = request.form['city']
			state = request.form['state']
			phoneNum = request.form['phoneNum']
			passportNo = request.form['passportNo']
			passportExp = request.form['passportExp']
			passportCty = request.form["passportCty"]
			dateOfBirth = request.form['dateOfBirth']
			ins = 'INSERT INTO customer(email, name, password, building_number, street, city, state, phone_number, \
						passport_number, passport_expiration, passport_country, date_of_birth) VALUES(%s, %s, %s, %s, %s, %s, %s, \
						%s, %s, %s, %s, %s)'
			cursor.execute(ins, (username, name, password, buildingNo, street, city, state, phoneNum, passportNo, \
										passportExp, passportCty, dateOfBirth))
			conn.commit()
		elif userType == "booking_agent":
			booking_agent_id = request.form['booking_agent_id']
			ins = 'INSERT INTO booking_agent (email, password, booking_agent_id) VALUES(%s, %s, %s)'
			cursor.execute(ins, (username, password, booking_agent_id))
			conn.commit()
		else:
			fname = request.form['fname']
			lname = request.form['lname']
			dateOfBirth = request.form['dateOfBirth']
			airline_name = request.form['airline_name']
			ins = 'INSERT INTO airline_staff(username, password, first_name, last_name, date_of_birth, airline_name) \
						VALUES(%s, %s, %s, %s, %s, %s)'
			cursor.execute(ins, (username, password, fname, lname, dateOfBirth, airline_name))
			conn.commit()
	return render_template('login.html')

@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	username = request.form['username']
	password = request.form['password']
	userType = request.form['usertype']
	password = calc_md5(password)

	if (userType == "airline_staff"):
		query = 'SELECT * FROM  airline_staff WHERE username = %s and password = %s'
	else:
		query = 'SELECT * FROM ' + userType + ' WHERE email = %s and password = %s'
	cursor.execute(query, (username, password))
	data = cursor.fetchone()
	error = None
	if (data):
		session['username'] = username
		session['type'] = userType
		conn.commit()
		return redirect("/")
	else:
		error = 'Invalid login.'
		return render_template('login.html', error=error)

@app.route('/addAirport', methods=['GET', 'POST'])
def addAirport():
	airport_name = request.form['airport_name']
	airport_city = request.form['airport_city']
	
	query = 'SELECT * FROM airport WHERE airport_name= %s'
	cursor.execute(query, airport_name)
	data = cursor.fetchone()
	if (data):
		message = "Airport already exists"
	else:
		ins = 'INSERT INTO airport(airport_name, airport_city) VALUES(%s, %s)'
		message = "Successfully Added"
		cursor.execute(ins, (airport_name, airport_city))
		conn.commit()
	return redirect(url_for('.index', message=message))

@app.route('/addPlane', methods=['GET', 'POST'])
def addPlane():
	airline_name = request.form['airline_name']
	airplane_id = request.form['airplane_id']
	seats = request.form['seats']

	airline = your_airline()

	if (airline_name == airline):
		query = 'SELECT * FROM airplane WHERE airline_name=%s and airplane_id=%s'
		cursor.execute(query, (airline_name, airplane_id))
		data = cursor.fetchone()

	try:
		if (data):
			message = "Airplane already exists"
		else:
			ins = 'INSERT INTO airplane(airline_name, airplane_id, seats) VALUES(%s, %s, %s)'
			message = "Successfully Added"
			cursor.execute(ins, (airline_name, airplane_id, seats))
			conn.commit()
	except Exception as e:
			if (str(e) == "local variable 'data' referenced before assignment"):
				message = "Please add your own airline's plane"
			else: 
				message = "No such airline exists"
	return redirect(url_for('.index', message=message))

@app.route('/createFlight', methods=['GET', 'POST'])
def createFlights():
	airline_name = request.form["airline_name"]
	flight_num = request.form["flight_num"]
	dpt_airport = request.form["dpt_airport"]
	dpt_time = request.form["dpt_time"]
	arr_airport = request.form["arr_airport"]
	arr_time = request.form["arr_time"]
	price = request.form["price"]
	status = request.form["status"]
	airplane_id = request.form["plane_id"]

	airline = your_airline()
	
	ins = 'INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
	try:
		if (airline_name == airline):
			cursor.execute(ins, (airline_name, flight_num, dpt_airport, dpt_time, arr_airport, dpt_time, price, status, airplane_id))
			conn.commit()
			message = "Successfully added"

		else: 
			message = "Please add your own airline's flight"
	except Exception as e:
		s = str(e).split(",", 1)[0]
		if (s == "(1452"):
			message = "Airline/airplaneID/Airport does not exist"
		elif (s == "(1062"):
			message = "Duplicate Entry"
	return redirect(url_for('.index', message=message))

@app.route('/updateStatus', methods=['GET', 'POST'])
def updateStatus():
	status = request.form['newStatus']
	airline_name = request.form['airline_name']
	flight_num = request.form['flight_num']
	query = 'UPDATE flight SET status = %s WHERE airline_name = %s AND flight_num = %s'
	cursor.execute(query, (status, airline_name, flight_num));
	conn.commit()
	return redirect("/")

@app.route("/search_flights", methods=['GET', 'POST'])
def search_flights():
	start_date = request.form["start_date"]
	end_date = request.form["end_date"]
	dpt_airport = request.form["dpt_airport"]
	arr_airport = request.form["arr_airport"]

	return redirect(url_for('.index', start_date=start_date, end_date=end_date, dpt_airport=dpt_airport, arr_airport=arr_airport))

@app.route('/filterFlightRevenue', methods=['GET', 'POST'])
def filterFlightRevenue():
	report_start_date = request.form['report_start_date']
	report_end_date = request.form['report_end_date']
	return redirect(url_for('.index', report_start_date=report_start_date, report_end_date=report_end_date))

@app.route('/homesearch', methods=['GET', 'POST'])
def home_search():
	departure_airport = request.form['Departure Airport']
	departure_city = request.form['Departure City']
	arrival_airport = request.form['Arrival Airport']
	arrival_city = request.form['Arrival City']
	date = request.form['Date']


	if len(departure_airport) > 0 and len(arrival_airport) > 0:
			airport = 'SELECT * FROM flight WHERE departure_airport = %s AND arrival_airport = %s AND date(departure_time) = %s'
			cursor.execute(airport, (departure_airport, arrival_airport, date))

	elif len(departure_airport) > 0 and len(arrival_airport) == 0:
			airport = 'SELECT * FROM flight WHERE departure_airport = %s AND date(departure_time) = %s AND arrival_airport = (SELECT airport_name FROM airport WHERE airport_city = %s)'
			cursor.execute(airport, (departure_airport, date, arrival_city))
		 
	elif len(departure_airport) == 0 and len(arrival_airport) > 0:
			airport = 'SELECT * FROM flight WHERE arrival_airport = %s AND date(departure_time) = %s AND departure_airport = (SELECT airport_name FROM airport WHERE airport_city = %s)'
			cursor.execute(airport, (arrival_airport, date, departure_city))
		 
	else:
			airport = 'SELECT * FROM flight WHERE date(departure_time) = %s AND departure_airport = (SELECT airport_name FROM airport WHERE airport_city = %s) and \
			arrival_airport = (SELECT airport_name FROM airport WHERE airport_city = %s)'
			cursor.execute(airport, (date, departure_city, arrival_city))

	flights = cursor.fetchall()
	userType = session['type']

	if (userType == "customer"):
		return render_template('search.html', flights=flights)
	else: 
		return render_template('search1.html', flights=flights)

@app.route('/purchase', methods=['GET', 'POST'])
def purchaseTicket():
	try:
		username = session['username']
		usertype = session['type']
		ticket_id = random.randint(0, 2147483647-1)
		purchase_date = date.today()
		if (usertype == "customer"):
			airline_name = request.form['airline_name']
			flight_num = request.form['flight_num']

			ins = 'INSERT INTO ticket VALUES(%s, %s, %s)'

			cursor.execute(ins, (ticket_id, airline_name, flight_num))
			conn.commit()
			ins = 'INSERT INTO purchases(ticket_id, customer_email, booking_agent_id, purchase_date) VALUES(%s, %s, NULL, %s)'
			cursor.execute(ins, (ticket_id, username, purchase_date))
		else:
			email = request.form["email"]

			cursor.execute('SELECT email FROM customer WHERE email=%s', email)
			data = cursor.fetchone()

			if (data):
				airline_name = request.form['airline_name']
				flight_num = request.form['flight_num']

				ins = 'INSERT INTO ticket VALUES(%s, %s, %s)'

				cursor.execute(ins, (ticket_id, airline_name, flight_num))
				conn.commit()
				cursor.execute("SELECT booking_agent_id FROM booking_agent WHERE email=%s", username)
				booking_agent_id = cursor.fetchone()['booking_agent_id']
				conn.commit()
				ins = 'INSERT INTO purchases(ticket_id, customer_email, booking_agent_id, purchase_date) VALUES(%s, %s, %s, %s)'
				message = "Success! You have purchased the ticket!"
				cursor.execute(ins, (ticket_id, email, booking_agent_id, purchase_date))
			else:
				raise ValueError('Cutsomer does not exists')

		return render_template("search.html", message=message, ticket_id=ticket_id)
	except Exception as e:
		print(e)
		if (str(e) == "Cutsomer does not exists"):
			error = "Cutsomer does not exists"
		else:
			error = "Please log in or register"
		if (usertype == "customer"):
			return render_template("search.html", error=error)
		else: 
			return render_template("search1.html", error=error)

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')

def create_pie_chart(start, end):
	airline = your_airline()
	cursor.execute('SELECT * FROM purchases NATURAL JOIN ticket WHERE purchase_date BETWEEN %s AND %s AND \
									airline_name=%s', (start, end, airline))
	puchases = cursor.fetchall()

	cust_revenue = 0
	agent_revenue = 0
	for bought in puchases:
		ticket_id = bought['ticket_id']
		cursor.execute('SELECT price FROM ticket NATURAL JOIN flight WHERE ticket_id=%s AND airline_name=%s', (ticket_id, airline))
		price = cursor.fetchone()['price']
		if (bought['booking_agent_id'] == None):
			cust_revenue += price
		else:
			agent_revenue += price
	total_revenue = agent_revenue + cust_revenue

	data = pd.Series([float(agent_revenue/total_revenue), float(cust_revenue/total_revenue)], index = ['Booking Agent', 'Customer'])
	pie_chart = Donut(data)
	pie_chart.toolbar_location = None
	info = [pie_chart, cust_revenue, agent_revenue]
	return info

def calc_md5(password):
	m = hashlib.md5() 
	m.update(password.encode(encoding = 'utf-8'))
	return m.hexdigest()

def your_airline():
	username = session['username']
	cursor.execute('SELECT airline_name FROM airline_staff WHERE username=%s', username)
	airline = cursor.fetchone()["airline_name"]
	return airline

def create_ticket_by_month(months_ticket, total):
	months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", \
																"November", "December"]
	plot = figure(x_range = months, y_range = (0, (total + 1) * 1.2), plot_height = 300, title="Tickets Purchased By Month")
	plot.xaxis.major_label_orientation = np.pi/4
	plot.vbar(x = months, top = months_ticket , width = 0.5, color = "#ff1200")
	plot.toolbar_location = None 
	return plot

def frequent_customer():
	first_day = date(date.today().year, 1, 1)
	last_day = date(date.today().year, 12, 31) 
	airline = your_airline()
	cursor.execute('SELECT * FROM (SELECT customer_email, COUNT(ticket_id) AS purchase_num FROM purchases NATURAL JOIN ticket \
									WHERE purchase_date BETWEEN %s AND %s AND airline_name = %s GROUP BY customer_email) AS T WHERE purchase_num = \
									(SELECT MAX(purchase_num))', (first_day, last_day, airline))
	top_customer = cursor.fetchone()
	return top_customer


app.secret_key = 'b\'e3r\xd7\xf4\xc7g\xd7N\xf5\xefV\xb9\xdf\xed\xf2P%~\t\x8f.X\x91'

if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
