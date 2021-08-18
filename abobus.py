# Основа для сайта, серверная часть

from flask import Flask, render_template, request, flash, redirect
import psycopg2 as ps
import psycopg2.extras


app = Flask(__name__)
app.config['SECRET_KEY'] = 'aboba'


DB_HOST = 'ec2-54-170-163-224.eu-west-1.compute.amazonaws.com'
DB_NAME = 'df043ppajn3au9'
DB_USER = 'lfcjpjxpmcfqxi'
DB_PASS = '70ec9d90f402e4102fb1ea1d8699a2a0c232034016d6edacd6d681093a20772b'
conn = ps.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/pricing')
def pricing():
    return render_template('pricing.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.method == 'POST':
            cur.execute('SELECT * FROM users')
            print(cur.fetchall())
            name = request.form.get('login')
            password = request.form.get('password')
            try:
                cur.execute('SELECT password FROM users WHERE login = %s', (name,))
                _pass = cur.fetchall()
                print(_pass)
                if _pass[0][0] == password:
                    cur.execute('SELECT login FROM users WHERE login = %s', (name,))
                    user = cur.fetchone()
                    user = user[0]
                    print(user)
                    flash('Вход был выполнен успешно', category='success')
                    return redirect('/pricing')

                else:
                    flash('Пароль или логин не совпадает', category='error')
            except Exception as e:
                print(e)
                flash('Такого аккаунта не существует, создайте его по ссылке ниже', category='error')
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('login')
        password = request.form.get('password')
        cur.execute('INSERT INTO users VALUES (%s,%s)', (str(name), str(password)))
        conn.commit()
        cur.execute('SELECT * FROM users')
        print(cur.fetchall())
        flash('Аккаунт успешно создан', category='success')
        return redirect('/login')
    return render_template('register.html')


@app.route('/update')
def update():
    return render_template('update_log.html')


if __name__ == '__main__':
    cur.execute("SELECT * FROM users")
    print(cur.fetchall())
    # cur.execute('CREATE TABLE IF NOT EXISTS users (login TEXT PRIMARY KEY, password TEXT)')
    app.run(debug=True)
