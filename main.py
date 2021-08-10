# Основа для сайта, серверная часть

from os import name
from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/pricing')
def pricing():
    return render_template('pricing.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/update')
def update():
    return render_template('update_log.html')


if __name__ == '__main__':
    app.run(debug=True)