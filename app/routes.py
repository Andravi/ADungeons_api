from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app.models.usuario import Usuario
from app import db, jwt
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
main_bp = Blueprint('main', __name__, url_prefix='/api')

@main_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Dados incompletos'}), 400
    
    if Usuario.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username já existe'}), 409
    
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email já cadastrado'}), 409
    
    try:
        usuario = Usuario(username=data['username'], email=data['email'])
        usuario.set_password(data['password'])
        ''
        db.session.add(usuario)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuário registrado com sucesso',
            'usuario': usuario.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username e password são obrigatórios'}), 400
    
    usuario = Usuario.query.filter_by(username=data['username']).first()
    
    if not usuario or not usuario.check_password(data['password']):
        return jsonify({'error': 'Credenciais inválidas'}), 401
    
    access_token = create_access_token(identity=usuario.id)
    
    usuario.update_last_login()
    
    return jsonify({
        'message': 'Login realizado com sucesso',
        'access_token': access_token,
        'usuario': usuario.to_dict()
    }), 200

@main_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    usuario = Usuario.query.get(current_user_id)
    
    return jsonify({
        'message': 'Acesso autorizado',
        'usuario': usuario.to_dict()
    }), 200

@main_bp.route('/testes', methods=['GET'])
# @jwt_required()
def get_users():
    # users = Usuario.query.all()
    return jsonify({
        'users': "[usuario.to_dict() for usuario in users]"
    }), 200