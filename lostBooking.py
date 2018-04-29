from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from datetime import date
from dateutil.relativedelta import relativedelta
import hashlib, random

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
    try:
      username = session['username']
      user = session['type']
      curr_date = date.today()
      one_months = date.today() + relativedelta(months=+1)
      cursor = conn.cursor()

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
                                    (curr_date, one_months, airline))
          print(e)
        flights = cursor.fetchall()

        cursor.execute('SELECT * FROM booking_agent')
        agents = cursor.fetchall()

        try:
          message = request.args['message']
          return render_template("airline_staff.html", flights=flights, agents=agents, username=username, airline=airline, message=message)
        except:
          return render_template("airline_staff.html", flights=flights, agents=agents, username=username, airline=airline)
      elif (user == "booking_agent"):
        cursor.execute('SELECT booking_agent_id FROM booking_agent WHERE email=%s', username)
        idnum = cursor.fetchone()["booking_agent_id"]
        return render_template("booking_agent.html", username=username, idnum=idnum)
      else: 
        return render_template("customer.html", username=username)
      conn.commit()
      cursor.close()
    except Exception as e:
      print(e)
      return render_template('index.html')
      
@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route('/registerAuth/<userType>', methods=['GET', 'POST'])
def registerAuth(userType):
    username = request.form['email']
    password = request.form['password']
    password = calc_md5(password)
    
    cursor = conn.cursor()

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
           cursor.execute(ins, (username, name, password, buildingNo, street, city, state, phoneNum, passportNo, 
            passportExp, passportCty, dateOfBirth))
       elif userType == "booking_agent":
           booking_agent_id = request.form['bookingAgentId']
           ins = 'INSERT INTO booking_agent (email, password, booking_agent_id) VALUES(%s, %s, %s)'
           cursor.execute(ins, (username, password, booking_agent_id))
       else:
           fname = request.form['fname']
           lname = request.form['lname']
           dateOfBirth = request.form['dateOfBirth']
           airline_name = request.form['airline_name']
           ins = 'INSERT INTO airline_staff(username, password, first_name, last_name, date_of_birth, airline_name) \
                VALUES(%s, %s, %s, %s, %s, %s)'
           cursor.execute(ins, (username, password, fname, lname, dateOfBirth, airline_name))
       conn.commit()
       cursor.close()
       
       return render_template('login.html')

@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
  username = request.form['username']
  password = request.form['password']
  userType = request.form['usertype']
  password = calc_md5(password)

  cursor = conn.cursor()
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
    cursor.close()
    return redirect("/")
  else:
    error = 'Invalid login.'
    return render_template('login.html', error=error)

@app.route('/addAirport', methods=['GET', 'POST'])
def addAirport():
  airport_name = request.form['airport_name']
  airport_city = request.form['airport_city']

  cursor = conn.cursor()
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
    cursor.close()
  return redirect(url_for('.index', message=message))

@app.route('/addPlane', methods=['GET', 'POST'])
def addPlane():
  airline_name = request.form['airline_name']
  airplane_id = request.form['airplane_id']
  seats = request.form['seats']

  cursor = conn.cursor()
  airline = your_airline()

  if (airline_name == airline):
    query = 'SELECT * FROM airplane WHERE airline_name= %s and airplane_id=%s'
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
      cursor.close()
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

  cursor = conn.cursor()
  airline = your_airline()
  
  ins = 'INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
  try:
    if (airline_name == airline):
      cursor.execute(ins, (airline_name, flight_num, dpt_airport, dpt_time, arr_airport, dpt_time, price, status, airplane_id))
      message = "Successfully added"
      uniqueId = True
      while (uniqueId):
        try: 
          ticket_num = random.randint(0, 10**11-1)
          cursor.execute('INSERT INTO ticket VALUES(%s, %s, %s)', (str(ticket_num), airline_name, flight_num))
          conn.commit()
          cursor.close()
          uniqueId = False
        except:
          pass
    else: 
      message = "Please add your own airline's flight"
  except Exception as e:
    print(e)
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
  cursor = conn.cursor()
  query = 'UPDATE flight SET status = %s WHERE airline_name = %s AND flight_num = %s'
  cursor.execute(query, (status, airline_name, flight_num));
  return redirect("/")

@app.route("/search_flights", methods=['GET', 'POST'])
def search_flights():
  start_date = request.form["start_date"]
  end_date = request.form["end_date"]
  dpt_airport = request.form["dpt_airport"]
  arr_airport = request.form["arr_airport"]

  return redirect(url_for('.index', start_date=start_date, end_date=end_date, dpt_airport=dpt_airport, arr_airport=arr_airport))


@app.route('/homesearch', methods=['GET', 'POST'])
def home_search():
  departure_airport = request.form['Departure Airport']
  departure_city = request.form['Departure City']
  arrival_airport = request.form['Arrival Airport']
  arrival_city = request.form['Arrival City']
  date = request.form['Date']

  cursor = conn.cursor()

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

  data = cursor.fetchall()
  cursor.close()
  return render_template('search.html', result = data)

@app.route('/search', methods=['GET', 'POST'])
def search():
    cursor = conn.cursor()
    cursor.close()
    return render_template('indexLoggedIn.html')


@app.route('/logout')
def logout():
  session.pop('username')
  return redirect('/')

def calc_md5(password):
  m = hashlib.md5()
  m.update(password.encode(encoding = 'utf-8'))
  return m.hexdigest()

def your_airline():
  username = session['username']
  cursor = conn.cursor()
  cursor.execute('SELECT airline_name FROM airline_staff WHERE username=%s', username)
  airline = cursor.fetchone()["airline_name"]
  return airline

app.secret_key = 'b\'e3r\xd7\xf4\xc7g\xd7N\xf5\xefV\xb9\xdf\xed\xf2P%~\t\x8f.X\x91'

if __name__ == "__main__":
  app.run('127.0.0.1', 5000, debug = True)
