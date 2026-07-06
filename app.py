from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'secret_key'

all_products = {}

@app.route('/', methods=['GET', 'POST'])
@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        category = request.form.get('category')

        price = float(price)

        if title in all_products:
            flash(f'Product {title} already exists!')
        else:
            all_products.update({title: {'price': price, 'category': category}})
            flash(f'Product {title} was added!')

        return redirect(url_for('products'))

    return render_template('product.html', products=all_products)


@app.route('/delete/<name_product>')
def delete(name_product):
    all_products.pop(name_product)
    flash(f'Product {name_product} was deleted!')
    return redirect(url_for('products'))


@app.route('/edit/<name_product>', methods=['GET', 'POST'])
def edit(name_product):
    product = all_products.get(name_product)

    if not product:
        flash(f'Product {name_product} not found!')
        return redirect(url_for('products'))

    if request.method == 'POST':
        price = request.form.get('price')
        category = request.form.get('category')

        product['price'] = float(price)
        product['category'] = category

        flash(f'Product {name_product} was updated!')
        return redirect(url_for('products'))

    return render_template('edit.html', name=name_product, product=product)


app.run(debug=True)
