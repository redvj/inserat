
from flask import url_for, jsonify, request
from app import app, db
from app.errors import bad_request
from app.models.login import User
from app.errors import error_response



@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin,
            'is_blocked': user.is_blocked,
            'avatar': user.avatar(100)  
        }
        user_list.append(user_data)
    return jsonify(user_list)

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user_data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin,
        'is_blocked': user.is_blocked,
        'avatar': user.avatar(100)  
    }
    return jsonify(user_data)



