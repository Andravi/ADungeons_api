from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app.models.campanha import Campanha
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


@main_bp.route('users/<string:email>', methods=['DELETE'])
def delete_user(email):
    try:
        # Busca e deleta o usuário diretamente
        user = Usuario.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": "Usuário não encontrado"}), 404
        
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {email} deletado com sucesso"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao deletar usuário: {str(e)}"}), 500


@main_bp.route('/login', methods=['POST'])
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


@auth_bp.route('/user/password', methods=['PUT'])
@jwt_required()
def change_password():
    # 1. Pegar dados da requisição
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    # 2. Validações básicas
    if not all([current_password, new_password]):
        return jsonify({"message": "Senha atual e nova senha são obrigatórias"}), 400

    # 3. Identificar usuário
    user_email = get_jwt_identity()
    user = Usuario.query.filter_by(id=user_email).first()

    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    # 4. Verificar senha atual
    if not user.check_password(current_password):
        return jsonify({"message": "Senha atual incorreta"}), 401

    # 5. Atualizar senha
    try:
        user.set_password(new_password)
        db.session.commit()
        return jsonify({"message": "Senha alterada com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao atualizar senha: {str(e)}"}), 500


@auth_bp.route('/campanhas', methods=['POST'])
@jwt_required()
def criar_campanha_autenticada():
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type deve ser application/json"}), 415

        data = request.get_json()
        user_id = get_jwt_identity()  # ID do usuário do token JWT

        if not data.get('name'):
            return jsonify({"error": "Nome da campanha é obrigatório"}), 400

        nova_campanha = Campanha(
            nome=data['name'],
            descricao=data.get('descricao', ''),
            id_mestre=user_id  # Associa ao usuário autenticado
        )

        db.session.add(nova_campanha)
        db.session.commit()

        return jsonify({
            "message": "Campanha criada com sucesso",
            "campanha": {
                "id": nova_campanha.id,
                "nome": nova_campanha.nome,
                "mestre": user_id
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@jwt.unauthorized_loader
def missing_auth_header_callback(error_string):
    return jsonify({
        "status": "error",
        "message": "Autenticação necessária, Acesso restrito a mestres logados",
        "details": "Por favor, inclua o token JWT no cabeçalho Authorization",
        "error_code": f"AUTH_HEADER_MISSING - {error_string}"
    }), 401