from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from datetime import date
from dateutil.relativedelta import relativedelta
import hashlib

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
      return render_template(user + '.html', username=username)
    except:
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

  cursor = conn.cursor()
  if (userType == "airline_staff"):
    query = 'SELECT * FROM  airline_staff WHERE username = %s and password = %s'
  else:
    query = 'SELECT * FROM ' + userType + ' WHERE email = %s and password = %s'

  cursor.execute(query, (username, password))
  data = cursor.fetchone()
  print(data);
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
    return render_template('airline_staff.html', message=message)
  else:
    ins = 'INSERT INTO airport(airport_name, airport_city) VALUES(%s, %s)'
    message = "Successfully Added"
    cursor.execute(ins, (airport_name, airport_city))
    conn.commit()
    cursor.close()
    return render_template('airline_staff.html', message=message)

@app.route('/addPlane', methods=['GET', 'POST'])
def addPlane():
  airline_name = request.form['airline_name']
  airplane_id = request.form['airplane_id']
  seats = request.form['seats']

  cursor = conn.cursor()
  query = 'SELECT * FROM airplane WHERE airline_name= %s and airplane_id=%s'
  cursor.execute(query, (airline_name, airplane_id))
  data = cursor.fetchone()

  try:
    if (data):
      message = "Airplane already exists"
      return render_template('airline_staff.html', message=message)
    else:
      ins = 'INSERT INTO airplane(airline_name, airplane_id, seats) VALUES(%s, %s, %s)'
      message = "Successfully Added"
      cursor.execute(ins, (airline_name, airplane_id, seats))
      conn.commit()
      cursor.close()
      return render_template('airline_staff.html', message=message)
  except:
      message = "No such airline exists"
      return render_template('airline_staff.html', message=message)

@app.route('/viewFlights', methods=['GET', 'POST'])
def viewFlights():
  curr_date = date.today()
  one_months = date.today() + relativedelta(months=+1)
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM flight WHERE departure_time BETWEEN %s AND %s', (curr_date, one_months))
  flights = cursor.fetchall()
  conn.commit()
  cursor.close()
  return render_template("airline_staff.html", flights=flights)

@app.route('/viewAgent', methods=['GET', 'POST'])
def viewAgent():
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM booking_agent')
  agents = cursor.fetchall()
  conn.commit()
  cursor.close()
  return render_template("airline_staff.html", agents=agents)

@app.route('/createFlight', methods=['GET', 'POST'])
def createFlights():
  return redirect("/")

@app.route('/updateStatus', methods=['GET', 'POST'])
def updateStatus():
  status = request.form['newStatus']
  airline_name = request.form['airline_name']
  flight_num = request.form['flight_num']
  print(status + " " + airline_name + " " + flight_num)
  cursor = conn.cursor()
  query = 'UPDATE flight SET status = %s WHERE airline_name = %s AND flight_num = %s'
  cursor.execute(query, (status, airline_name, flight_num));
  return redirect("/")

@app.route('/logout')
def logout():
  session.pop('username')
  return redirect('/')

def calc_md5(password):
  m = hashlib.md5()
  m.update(password.encode(encoding = 'utf-8'))
  return m.hexdigest()

app.secret_key = 'b\'e3r\xd7\xf4\xc7g\xd7N\xf5\xefV\xb9\xdf\xed\xf2P%~\t\x8f.X\x91'

if __name__ == "__main__":
  app.run('127.0.0.1', 5000, debug = True)
