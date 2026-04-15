"""
Web Development - Template Rendering Example
"""

from flask import Flask, render_template_string, request, redirect, url_for, session
from typing import Dict, List

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session management


# HTML Templates
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Template Demo{% endblock %}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
               background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
               min-height: 100vh; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; background: white; 
                   border-radius: 10px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        h1 { color: #333; margin-bottom: 20px; }
        h2 { color: #667eea; margin: 15px 0; }
        .nav { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .nav a { color: #667eea; text-decoration: none; margin-right: 20px; font-weight: 500; }
        .nav a:hover { text-decoration: underline; }
        .card { border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin: 15px 0; 
                transition: transform 0.2s; }
        .card:hover { transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .btn { background: #667eea; color: white; border: none; padding: 10px 20px; 
               border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; }
        .btn:hover { background: #5568d3; }
        .form-group { margin: 15px 0; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 500; }
        .form-group input, .form-group textarea, .form-group select { 
            width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .alert { padding: 15px; border-radius: 5px; margin: 15px 0; }
        .alert-success { background: #d4edda; color: #155724; }
        .alert-error { background: #f8d7da; color: #721c24; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #667eea; color: white; }
        tr:hover { background: #f5f5f5; }
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="/">Home</a>
            <a href="/products">Products</a>
            <a href="/cart">Cart ({{ cart|length }})</a>
            {% if session.get('user') %}
                <a href="/logout">Logout ({{ session.user }})</a>
            {% else %}
                <a href="/login">Login</a>
            {% endif %}
        </div>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

HOME_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
{% block content %}
<h1>Welcome to Template Demo</h1>
<p>This is a demonstration of Flask template rendering with various features.</p>

<h2>Features Demonstrated:</h2>
<div class="card">
    <h3>🎨 Template Inheritance</h3>
    <p>Base template with blocks for content customization</p>
</div>

<div class="card">
    <h3>📦 Product Management</h3>
    <p>CRUD operations with form handling</p>
</div>

<div class="card">
    <h3>🛒 Shopping Cart</h3>
    <p>Session-based cart functionality</p>
</div>

<div class="card">
    <h3>👤 User Authentication</h3>
    <p>Login system with session management</p>
</div>

<div class="card">
    <h3>📊 Data Display</h3>
    <p>Tables, loops, and conditional rendering</p>
</div>

<a href="/products" class="btn">View Products</a>
{% endblock %}
""")

PRODUCTS_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
{% block title %}Products{% endblock %}
{% block content %}
<h1>Products</h1>

{% if products %}
<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Price</th>
            <th>Category</th>
            <th>Stock</th>
            <th>Action</th>
        </tr>
    </thead>
    <tbody>
        {% for product in products %}
        <tr>
            <td>{{ product.name }}</td>
            <td>${{ "%.2f"|format(product.price) }}</td>
            <td>{{ product.category }}</td>
            <td>{{ product.stock }}</td>
            <td>
                <a href="/add_to_cart/{{ product.id }}" class="btn">Add to Cart</a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% else %}
<p>No products available.</p>
{% endif %}

<h2>Add New Product</h2>
<form action="/products" method="POST">
    <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>
    </div>
    <div class="form-group">
        <label for="price">Price:</label>
        <input type="number" id="price" name="price" step="0.01" required>
    </div>
    <div class="form-group">
        <label for="category">Category:</label>
        <select id="category" name="category" required>
            <option value="Electronics">Electronics</option>
            <option value="Clothing">Clothing</option>
            <option value="Books">Books</option>
            <option value="Home">Home</option>
        </select>
    </div>
    <div class="form-group">
        <label for="stock">Stock:</label>
        <input type="number" id="stock" name="stock" required>
    </div>
    <button type="submit" class="btn">Add Product</button>
</form>
{% endblock %}
""")

CART_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
{% block title %}Shopping Cart{% endblock %}
{% block content %}
<h1>Shopping Cart</h1>

{% if cart %}
    <table>
        <thead>
            <tr>
                <th>Product</th>
                <th>Price</th>
                <th>Quantity</th>
                <th>Total</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            {% for item in cart %}
            <tr>
                <td>{{ item.name }}</td>
                <td>${{ "%.2f"|format(item.price) }}</td>
                <td>{{ item.quantity }}</td>
                <td>${{ "%.2f"|format(item.price * item.quantity) }}</td>
                <td>
                    <a href="/remove_from_cart/{{ item.id }}" class="btn">Remove</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <h2>Total: ${{ "%.2f"|format(total) }}</h2>
    
    <a href="/checkout" class="btn">Checkout</a>
    <a href="/clear_cart" class="btn">Clear Cart</a>
{% else %}
    <p>Your cart is empty.</p>
    <a href="/products" class="btn">Continue Shopping</a>
{% endif %}
{% endblock %}
""")

LOGIN_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
{% block title %}Login{% endblock %}
{% block content %}
<h1>Login</h1>

<form action="/login" method="POST">
    <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>
    </div>
    <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
    </div>
    <button type="submit" class="btn">Login</button>
</form>

<p>Demo credentials: username: <strong>admin</strong>, password: <strong>password</strong></p>
{% endblock %}
""")

# In-memory data storage
products_db = [
    {'id': 1, 'name': 'Laptop', 'price': 999.99, 'category': 'Electronics', 'stock': 50},
    {'id': 2, 'name': 'Mouse', 'price': 29.99, 'category': 'Electronics', 'stock': 200},
    {'id': 3, 'name': 'T-Shirt', 'price': 19.99, 'category': 'Clothing', 'stock': 100},
    {'id': 4, 'name': 'Python Book', 'price': 39.99, 'category': 'Books', 'stock': 30}
]

product_id_counter = 5


# Routes
@app.route('/')
def home():
    """Home page"""
    return render_template_string(HOME_TEMPLATE)


@app.route('/products', methods=['GET', 'POST'])
def products():
    """Products page with CRUD operations"""
    global product_id_counter
    
    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        category = request.form.get('category')
        stock = int(request.form.get('stock'))
        
        new_product = {
            'id': product_id_counter,
            'name': name,
            'price': price,
            'category': category,
            'stock': stock
        }
        products_db.append(new_product)
        product_id_counter += 1
        
        return redirect(url_for('products'))
    
    return render_template_string(PRODUCTS_TEMPLATE, products=products_db)


@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    """Add product to cart"""
    product = next((p for p in products_db if p['id'] == product_id), None)
    if product:
        cart = session.get('cart', [])
        
        # Check if product already in cart
        existing_item = next((item for item in cart if item['id'] == product_id), None)
        if existing_item:
            existing_item['quantity'] += 1
        else:
            cart.append({
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'quantity': 1
            })
        
        session['cart'] = cart
    
    return redirect(url_for('products'))


@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    """Remove product from cart"""
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    """Shopping cart page"""
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    
    return render_template_string(CART_TEMPLATE, cart=cart, total=total)


@app.route('/clear_cart')
def clear_cart():
    """Clear shopping cart"""
    session.pop('cart', None)
    return redirect(url_for('cart'))


@app.route('/checkout')
def checkout():
    """Checkout page"""
    if 'cart' not in session or not session['cart']:
        return redirect(url_for('products'))
    
    session.pop('cart', None)
    return "Thank you for your purchase! <a href='/'>Return to Home</a>"


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'password':
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid credentials. <a href='/login'>Try again</a>"
    
    return render_template_string(LOGIN_TEMPLATE)


@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.pop('user', None)
    return redirect(url_for('home'))


def main():
    """Main function to demonstrate template rendering"""
    print("Flask Template Rendering Example")
    print("=" * 50)
    
    print("\nTemplate Rendering Features:")
    print("✓ Template inheritance with base templates")
    print("✓ Block system for content customization")
    print("✓ Variable interpolation and filters")
    print("✓ Control structures (if, for loops)")
    print("✓ Form handling and validation")
    print("✓ Session management")
    print("✓ Flash messages for user feedback")
    print("✓ URL generation with url_for()")
    print("✓ Dynamic content rendering")
    
    print("\nTo run this application:")
    print("1. Install Flask: pip install flask")
    print("2. Run: python template_rendering.py")
    print("3. Access: http://127.0.0.1:5000")
    
    print("\nDemo Pages:")
    print("  / - Home page with feature overview")
    print("  /products - Product management")
    print("  /cart - Shopping cart")
    print("  /login - User login")
    print("\nDemo Credentials:")
    print("  Username: admin")
    print("  Password: password")


if __name__ == "__main__":
    main()
    
    # To actually run the server, uncomment the following:
    # app.run(debug=True, host='127.0.0.1', port=5000)