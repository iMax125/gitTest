from flask import Flask, render_template, request, flash, redirect, url_for, session
from models import init_db, Product, Company
from actions_db import *
import re

app = Flask(__name__)
app.secret_key = 'secret_key'

# підключення до БД
init_db()


def validate_password(password):
    if len(password) < 6:
        return "Пароль має бути не коротший за 6 символів!"
    if not re.search(r"[A-Za-z]", password):
        return "Пароль має містити хоча б одну літеру!"
    if not re.search(r"[0-9]", password):
        return "Пароль має містити хоча б одну цифру!"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Пароль має містити хоча б один спецсимвол!"
    return None


@app.route('/', methods=['GET', 'POST'])
@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        category = request.form.get('category')

        price = float(price)

        if product_exists(title):
            flash(f'Product {title} already exists!')
        else:
            add_product(title, price, category)
            flash(f'Product {title} was added!')

        return redirect(url_for('products'))

    all_categories = get_categories()
    choose_category = request.args.get('category', 'all')

    if choose_category == 'all':
        filter_products = get_products()
    else:
        filter_products = get_products_by_category(choose_category)

    return render_template('product.html',
                           products=filter_products,
                           categories=all_categories,
                           choose_category=choose_category)


@app.route('/delete/<name_product>')
def delete(name_product):
    delete_product(name_product)
    flash(f'Product {name_product} was deleted!')
    return redirect(url_for('products'))


@app.route('/edit/<name_product>', methods=['GET', 'POST'])
def edit(name_product):
    product = Product.select().where(Product.name == name_product).first()

    if not product:
        flash("Product not found!")
        return redirect(url_for('products'))

    if request.method == 'POST':
        new_price = float(request.form.get('price'))
        new_category = request.form.get('category')

        edit_product(name_product, new_price, new_category)
        flash("Product updated!")
        return redirect(url_for('products'))

    return render_template('edit.html', product=product)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        if not login:
            flash("Логін не може бути порожнім!")
            return redirect(url_for('register'))

        error = validate_password(password)
        if error:
            flash(error)
            return redirect(url_for('register'))

        if Company.select().where(Company.login == login).exists():
            flash("Такий логін вже існує!")
            return redirect(url_for('register'))

        Company.create(login=login, password=password)
        flash("Реєстрація успішна! Увійдіть у систему.")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        user = Company.select().where(
            (Company.login == login) & (Company.password == password)
        ).first()

        if not user:
            flash("Невірний логін або пароль!")
            return redirect(url_for('login'))

        session['user'] = login
        flash("Ви увійшли!")
        return redirect(url_for('products'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Ви вийшли з системи!")
    return redirect(url_for('login'))


app.run(debug=True)
