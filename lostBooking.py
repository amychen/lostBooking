from flask import Flask, render_template, url_for
from jinja2 import Template

app = Flask(__name__)

@app.route("/")
def init():
    return render_template('register.html')