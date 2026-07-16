from models import Product

'''create'''
def add_product(name: str, price: float, category: str):
    Product.create(name=name, price=price, category=category)

'''read'''

def get_categories():
    products = Product.select(Product.category).distinct().order_by(Product.category)
    categories = [product.category for product in products]
    return categories

def get_products():
    return Product.select()

def get_products_by_category(category: str):
    return Product.select().where(Product.category == category)

def product_exists(name: str) -> bool:
    return Product.select().where(Product.name == name).exists()


'''update'''

def edit_product(name: str, new_price: float, new_category: str):
    query = Product.update(price=new_price, category=new_category).where(Product.name == name)
    query.execute()


'''delete'''

def delete_product(name: str):
    query = Product.delete().where(Product.name == name)
    query.execute()
