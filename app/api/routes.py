from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Todo, Todo_schema, Todos_schema

api = Blueprint('api',__name__, url_prefix='/api')

# @api.route('/getdata')
# def getdata():
#     return {'yee': 'haw'}

@api.route('/todo', methods = ['POST'])
@token_required
def create_todo(current_user_token):
    to_do = request.json['to_do']
    when = request.json['when']
    where = request.json['where']
    w_who = request.json['w_who']
    how_long = request.json['how_long']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    todo = Todo(to_do, when, where, w_who, how_long, user_token=user_token)

    db.session.add(todo)
    db.session.commit()

    response = Todo_schema.dump(todo)
    return jsonify(response)

@api.route('/todo', methods = ['GET'])
@token_required
def get_todo(current_user_token):
    a_user = current_user_token.token
    to_dos = Todo.query.filter_by(user_token = a_user).all()
    response = Todos_schema.dump(to_dos)
    return jsonify(response)

# Optional! Might not work 
# @api.route('/contacts/<id>', methods = ['GET'])
# @token_required
# def get_single_contact(current_user_token, id):
#     contact = Contact.query.get(id)
#     repsonse = contact_schema.dump(contact)
#     return jsonify(response)


#Updating
@api.route('/todo/<id>', methods = ['POST', 'PUT'])
@token_required
def update_todo(current_user_token, id):
    todo = Todo.query.get(id)
    todo.to_do = request.json['to_do']
    todo.when = request.json['when']
    todo.where = request.json['where']
    todo.w_who = request.json['w_who']
    todo.how_long = request.json['how_long']
    todo.user_token = current_user_token.token 

    db.session.commit()
    response = Todo_schema.dump(todo)
    return jsonify(response)


#Delete Endpoint
@api.route('/todo/<id>', methods = ['DELETE'])
@token_required
def delete_tool(current_user_token, id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    response = Todo_schema.dump(todo)
    return jsonify(response)
