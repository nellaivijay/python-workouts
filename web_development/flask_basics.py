"""
Web Development - Flask Basics Example
"""

from flask import Flask, jsonify, request, render_template_string
from typing import Dict, List

app = Flask(__name__)

# Sample data storage (in-memory for demonstration)
users_db: Dict[int, Dict] = {}
user_id_counter = 1

# HTML template for demonstration
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask Demo</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .user { border: 1px solid #ddd; padding: 10px; margin: 10px 0; border-radius: 5px; }
        .form { margin: 20px 0; }
        input { padding: 5px; margin: 5px; }
        button { padding: 8px 15px; background: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <h1>Flask Web Application Demo</h1>
    
    <div class="form">
        <h2>Add New User</h2>
        <form action="/users" method="POST">
            <input type="text" name="name" placeholder="Name" required>
            <input type="email" name="email" placeholder="Email" required>
            <input type="number" name="age" placeholder="Age">
            <button type="submit">Add User</button>
        </form>
    </div>
    
    <h2>Users List</h2>
    <div id="users">
        {% for user in users %}
        <div class="user">
            <strong>{{ user.name }}</strong> ({{ user.email }})
            <br>Age: {{ user.age }}
            <br>ID: {{ user.id }}
        </div>
        {% endfor %}
    </div>
    
    <div style="margin-top: 30px;">
        <h3>API Endpoints:</h3>
        <ul>
            <li>GET / - HTML interface</li>
            <li>GET /api/users - Get all users (JSON)</li>
            <li>POST /api/users - Create user (JSON)</li>
            <li>GET /api/users/&lt;id&gt; - Get specific user</li>
            <li>PUT /api/users/&lt;id&gt; - Update user</li>
            <li>DELETE /api/users/&lt;id&gt; - Delete user</li>
        </ul>
    </div>
</body>
</html>
"""


@app.route('/')
def home():
    """Home route with HTML interface"""
    users_list = list(users_db.values())
    return render_template_string(HTML_TEMPLATE, users=users_list)


@app.route('/users', methods=['POST'])
def create_user_html():
    """Create user via HTML form"""
    global user_id_counter
    
    name = request.form.get('name')
    email = request.form.get('email')
    age = request.form.get('age', type=int)
    
    if name and email:
        user = {
            'id': user_id_counter,
            'name': name,
            'email': email,
            'age': age
        }
        users_db[user_id_counter] = user
        user_id_counter += 1
        
        users_list = list(users_db.values())
        return render_template_string(HTML_TEMPLATE, users=users_list)
    
    return "Error: Name and email are required", 400


# API Routes
@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users - API endpoint"""
    return jsonify(list(users_db.values()))


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    """Get specific user - API endpoint"""
    user = users_db.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404


@app.route('/api/users', methods=['POST'])
def create_user_api():
    """Create new user - API endpoint"""
    global user_id_counter
    
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Name and email are required'}), 400
    
    user = {
        'id': user_id_counter,
        'name': data['name'],
        'email': data['email'],
        'age': data.get('age')
    }
    
    users_db[user_id_counter] = user
    user_id_counter += 1
    
    return jsonify(user), 201


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id: int):
    """Update user - API endpoint"""
    user = users_db.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        user['name'] = data['name']
    if 'email' in data:
        user['email'] = data['email']
    if 'age' in data:
        user['age'] = data['age']
    
    return jsonify(user)


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    """Delete user - API endpoint"""
    user = users_db.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    del users_db[user_id]
    return jsonify({'message': 'User deleted successfully'})


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'total_users': len(users_db),
        'version': '1.0.0'
    })


def add_sample_data():
    """Add sample data for demonstration"""
    global user_id_counter
    sample_users = [
        {'name': 'Alice Johnson', 'email': 'alice@example.com', 'age': 28},
        {'name': 'Bob Smith', 'email': 'bob@example.com', 'age': 35},
        {'name': 'Charlie Brown', 'email': 'charlie@example.com', 'age': 42}
    ]
    
    for user_data in sample_users:
        user = {
            'id': user_id_counter,
            **user_data
        }
        users_db[user_id_counter] = user
        user_id_counter += 1


def main():
    """Main function to run the Flask application"""
    print("Flask Web Application")
    print("=" * 50)
    
    # Add sample data
    add_sample_data()
    print(f"Added {len(users_db)} sample users")
    
    print("\nStarting Flask server...")
    print("Access the application at: http://127.0.0.1:5000")
    print("\nAvailable endpoints:")
    print("  GET  / - HTML interface")
    print("  GET  /api/users - Get all users")
    print("  POST /api/users - Create user")
    print("  GET  /api/users/<id> - Get specific user")
    print("  PUT  /api/users/<id> - Update user")
    print("  DELETE /api/users/<id> - Delete user")
    print("  GET  /api/health - Health check")
    
    # Run the application
    app.run(debug=True, host='127.0.0.1', port=5000)


if __name__ == '__main__':
    # For demonstration purposes, we'll show the code structure
    # In production, you would run: python flask_basics.py
    print("Flask Web Application Example")
    print("=" * 50)
    print("\nThis script demonstrates:")
    print("✓ Flask application setup")
    print("✓ HTML template rendering")
    print("✓ RESTful API endpoints")
    print("✓ CRUD operations")
    print("✓ Form handling")
    print("✓ JSON responses")
    print("\nTo run this application:")
    print("1. Install Flask: pip install flask")
    print("2. Run: python flask_basics.py")
    print("3. Access: http://127.0.0.1:5000")
    print("\nNote: Remove the main() call guard above to actually run the server")