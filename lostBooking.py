from flask import Flask, render_template, url_for
from flask.ext.mysqldb import MySQL

app = Flask(__name__)
conn = pymysql.connect(host='localhost',
                       user='root',
                       port = 8889,
                       password='root',
                       db='flight_ticket_system',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
mysql = MySQL(app)

@app.route("/")
def init():
    cur = mysql.connection.cursor()
    return render_template('register.html')

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)