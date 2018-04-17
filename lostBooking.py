from flask import Flask, render_template, url_for
from flask.ext.mysqldb import MySql

app = Flask(__name__)
conn = pymysql.connect(host='localhost',
                       user='root',
                       port = 8889,
                       password='root',
                       db='flight_ticket_system',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

@app.route("/")
def init():
    return render_template('register.html')