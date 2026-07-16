from flask import Flask, render_template, request, flash, redirect, url_for
from models import init_db, Product
from actions_db import *

app = Flask(__name__)
app.secret_key = 'secret_key'

# підключення до БД
init_db()


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

    # актуальні категорії на основі товарів
    all_categories = get_categories()

    # обрана категорія
    choose_category = request.args.get('category', 'all')

    if choose_category == 'all':
        filter_products = get_products()
    else:
        # фільтрація
        filter_products = get_products_by_category(choose_category)

    return render_template('product.html',
                           products=filter_products,
                           categories=all_categories,
                           choose_category=choose_category)


# динамічне посилання з параметрами <>
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


app.run(debug=True)
