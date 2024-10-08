# Основа для сайта, серверная часть
# import psycopg2 as ps
# import psycopg2.extras
# DB_HOST = 'ec2-54-170-163-224.eu-west-1.compute.amazonaws.com'
# DB_NAME = 'df043ppajn3au9'
# DB_USER = 'lfcjpjxpmcfqxi'
# DB_PASS = '70ec9d90f402e4102fb1ea1d8699a2a0c232034016d6edacd6d681093a20772b'
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, login_required, logout_user, current_user, LoginManager
from random import randint, choice
from p_redact import clear as clean
import os

back = '<script>document.location.href = document.referrer</script>'

db_info = {
    'user': 'lfcjpjxpmcfqxi',
    'password': '70ec9d90f402e4102fb1ea1d8699a2a0c232034016d6edacd6d681093a20772b',
    'host': 'ec2-54-170-163-224.eu-west-1.compute.amazonaws.com',
    'db_name': 'df043ppajn3au9'
}

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "postgresql://lfcjpjxpmcfqxi:70ec9d90f402e4102fb1ea1d8699a2a0c232034016d6edacd6d681093a20772b@ec2-54-170-163-224.eu-west-1.compute.amazonaws.com:5432/df043ppajn3au9"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# CTG: Модели таблиц
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    login = db.Column(db.String(), unique=True)
    password = db.Column(db.String())

    def __init__(self, id, login, password):
        self.id = id
        self.login = login
        self.password = password

    def get_id(self):
        return (self.id)


class Product(db.Model):
    __tablename__ = 'production'

    name = db.Column(db.String(), unique=True, primary_key=True)
    price = db.Column(db.String())
    description = db.Column(db.String())
    avatarUrl = db.Column(db.String())
    long = db.Column(db.String())
    zametki = db.Column(db.String())
    category = db.Column(db.String())

    def __init__(self, name, price, description, avatarUrl, long, zametki, category):
        self.name = name
        self.price = price
        self.description = description
        self.avatarUrl = avatarUrl
        self.long = long
        self.zametki = zametki
        self.category = category

class Partner(db.Model):
    __tablename__ = 'partners'

    name = db.Column(db.String(), unique=True, primary_key=True)
    description = db.Column(db.String())
    avatarUrl = db.Column(db.String())
    members = db.Column(db.Integer())

    def __init__(self, name, description, avatarUrl, members):
        self.name = name
        self.description = description
        self.avatarUrl = avatarUrl
        self.members = members


# CTG: главная страница
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('main.html', user=current_user)

#
# CTG: Партнерства
@app.route('/partnerships', methods=['POST', 'GET'])
def partners():
    partnerships = Partner.query.all()
    return render_template('partnerships.html', user=current_user, parthnersities=partnerships)



# CTG: Страницы покупок
@app.route('/pricing', methods=['POST', 'GET'])
def pricing():
    products = Product.query.filter_by(category='tovar')
    cars = Product.query.filter_by(category='cars')
    return render_template('pricing.html', user=current_user, products=products, cars=cars)


@app.route('/pricing/<string:name>', methods=['POST', 'GET'])
def shop(name):
    product = Product.query.filter_by(name=name).first()
    return render_template('product.html', user=current_user, product=product)


# CTG: Логин регистрация
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            name = request.form.get('login')
            password = request.form.get('password')
            user = User.query.filter_by(login=name).first()
            if user:
                try:
                    if user.password == password:
                        login_user(user)
                        flash('Вход успешен', category='success')
                        return redirect(f'/home/{user.login}')
                    else:
                        flash('Пароль или логин неверен', category='error')
                except Exception as e:
                    print(e)
            else:
                flash('Аккаунта не существует, зарегистрируйтесь по ссылке ниже', category='error')
        except Exception as e:
            print(e)
            flash(f'{e}', category='error')
    flash('Страница входа | регистрации временно не работает', category='error')
    return render_template('admin.html', user=current_user)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            name = request.form.get('login')
            password = request.form.get('password')
            user = User.query.filter_by(login=name).first()
            if user:
                flash('Аккаунт уже существует', category='error')
            else:
                try:
                    new_user = User(id=randint(1, 99999), login=name, password=password)
                    login_user(new_user, remember=True)
                    print(new_user)
                    db.session.add(new_user)
                    db.session.commit()
                    flash('Аккаунт успешно создан', category='success')
                    return redirect(f'/home/{new_user.login}')
                except Exception as e:
                    flash(f'Ошибка на сервере: {e}', category='error')
                    print(e)
        except Exception as e:
            print(e)
            flash('Аккаунт уже существует', category='error')
    return render_template('register.html', user=current_user)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect('/')


# CTG: "админ" страницы
@app.route('/redact', methods=['POST', 'GET'])
def redact():
    if request.method == 'POST':
        name = request.form.get('name')
        object = request.form.get('object')
        new = request.form.get('new')
        print(f'{name} \n{object} \n{new}')
        try:
            product = Product.query.filter_by(name=name).first()
            if object.lower() == 'name':
                product.name = new
            elif object.lower() == 'price':
                product.price = new
            elif object.lower() == 'description':
                product.description = new
            elif object.lower() == 'url' or 'avatarUrl':
                product.avatarUrl = new
            elif object.lower() == 'long':
                product.long = new
            elif object.lower() == 'zametki':
                product.zametki = new
            elif object.lower() == 'category' or 'cat':
                product.category = new
            db.session.commit()
            flash('Данные успешно обновлены', category='success')
        except Exception as e:
            print(e)
            flash(e)
    return render_template('redact.html', user=current_user, products=Product.query.all())


@app.route('/home/<string:login>/', methods=['POST', 'GET'])
@login_required
def user_home(login):
    citats = [
        'Устал после gym? Присаживайся и выпей чашечку cum!',
        'Задолбали fucking slaves? Болит рука? Сходи к Jabronies!',
        'Завтра снова в gym, а накопленного cum не хватает?\nВ  нашем магазине есть много cum по выгодным скидкам!',
        'Эти fucking slaves опять порвали твой bondage? Получи бесплатный в нашем магазине!'
    ]
    ment = choice(citats)
    return render_template('user.html', nickname=login, user=current_user, ment=ment)


@app.route('/home/sanekakf/create', methods=['POST', 'GET'])
@login_required
def create_product():
    if current_user.login != 'sanekakf':
        raise 404
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        long = request.form.get('long')
        description = request.form.get('description')
        zametki = request.form.get('zametka')
        avatarUrl = request.form.get('url')
        category = request.form.get('category')
        new_tovar = Product(name=name, price=price, long=long, description=description, zametki=zametki, avatarUrl=avatarUrl, category=category.lower())
        db.session.add(new_tovar)
        db.session.commit()
    return render_template('creation.html', user=current_user)


@app.route('/home/sanekakf/clear', methods=['POST', 'GET'])
def clear():
    clean()
    return redirect(url_for('pricing'))


# CTG: "страницы людей"
@app.route('/users', methods=['POST', 'GET'])
def users():
    persons = User.query.all()
    print(persons)
    return render_template('users.html', user=current_user, users=persons)


@app.route('/users/delete/<string:username>/', methods=['POST', 'GET'])
def u_delete(username):
    try:
        User.query.filter_by(login=username).delete()
        db.session.commit()
        flash(f'{username} удалён', category='success')
    except Exception as e:
        print(e)
        flash(e)
    return back


# CTG: Доп. файлы
@app.route('/pictures', methods=['POST', 'GET'])
def pictures():
    return render_template('pictures.html', user=current_user)


# CTG: обработка ошибочных страниц
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('505.html'), 500


# CTG: Ретёрнывые функции
@app.route('/delete/<string:name>/', methods=['GET', 'POST'])
def delete(name):
    try:
        Product.query.filter_by(name=name).delete()
        db.session.commit()
        flash(f'Предмет {name} был успешно удален!', category='success')
    except Exception as e:
        print(e)
        flash('Ошибка', category='error')
    return back


# CTG: Одиночные страницы
@app.route('/about', methods=['POST', 'GET'])
def about():
    return render_template('about.html', user=current_user)


if __name__ == '__main__':
    db.session.flush()
    login_manager = LoginManager(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(user_id)
        except Exception as e:
            print(e)
            return None

    login_manager.init_app(app)
    app.run(debug=True, host='0.0.0.0', port=5000)
